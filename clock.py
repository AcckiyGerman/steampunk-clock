import datetime
from time import sleep
from RPi import GPIO

# инифиализируем гребенку на выход и посылаем туда False (на выходе будет 0 вольт)
GPIO.setmode(GPIO.BCM)
for i in range(1, 11):
    GPIO.setup(i, GPIO.OUT)
    sleep(0.05)
    GPIO.output(i, False)

# цифры-разряды наших часов, всего 6 ламп
digits = [0, 0,  # hour
          0, 0,  # minute
          0, 0]  # second


def set_digit(digit, value):
    """switch on digit through GPIO. Function using only 6 digits: 0-5."""
    """Appropriate GPIO 1-6"""
    # нумерация GPIO начинается с 1, а массив digits,
    # которые их представляют - с 0. Поэтому:
    digit += 1
    # вначале потушим лампу, которая сейчас горит:
    previous_digit = 6 if digit == 1 else digit - 1
    GPIO.output(previous_digit, False)
    # теперь зажжем нужную
    GPIO.output(digit, True)
    send_value_to_decoder(value)


def send_value_to_decoder(value):
    """кодирует цифру 0-9 в 4-битное число и посылает его на GPIO 7-10"""
    # 0->7 1->8 2->9 3->10

    bit_view = bin(value + 16)
    print(bit_view)

# main cycle
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
