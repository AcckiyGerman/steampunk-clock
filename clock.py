import datetime
from time import sleep
from RPi import GPIO
# инициализируем GPIO на выход и посылаем туда False (на выходе будет 0 вольт)
GPIO.setmode(GPIO.BCM)
for i in range(1, 11):
    GPIO.setup(i, GPIO.OUT)
    sleep(0.05)
    GPIO.output(i, False)
# цифры-разряды наших часов, моделирует лампы устройства. Всего 6 ламп: ЧЧ ММ СС
digits = [0]*6
# таблица двоичных чисел для декодера:
encoded = ['0000', '0001', '0010', '0011', '0100', '0101', '0110', '0111', '1000', '1001']


def set_digit(digit, value):
    """switch on digit through GPIO"""
    # нумерация GPIO 1-6, а массив digits, который представляет лампы 0-5. Поэтому:
    digit += 1
    # вначале потушим лампу, которая сейчас горит:
    previous_lamp = 6 if digit == 1 else digit - 1
    GPIO.output(previous_lamp, False)
    # теперь зажжем нужную
    GPIO.output(digit, True)
    send_value_to_decoder(value)


def send_value_to_decoder(number):
    """кодирует цифру 0-9 в 4-битное число и посылает его на GPIO 7-10
    Соответствие: разряд_числа -> GPIO:  0->7 1->8 2->9 3->10 """
    code = encoded[number]
    GPIO.output(7, code[0])
    GPIO.output(8, code[1])
    GPIO.output(9, code[2])
    GPIO.output(10, code[3])

while True:
    now = datetime.datetime.now()
    hour, minute, second = now.hour, now.minute, now.second
    digits[0] = hour // 10
    digits[1] = hour % 10
    digits[2] = minute // 10
    digits[3] = minute % 10
    digits[4] = second // 10
    digits[5] = second % 10
    # будем выводить полученные цифры пока не наступит следующая секунда
    while datetime.datetime.now() < now + datetime.timedelta(seconds=1):
        print('\r', digits, end='')  # console log
        for key, value in enumerate(digits):
            set_digit(key, value)
            sleep(0.0008)