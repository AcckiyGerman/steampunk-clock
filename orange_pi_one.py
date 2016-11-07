import datetime
from time import sleep
from pyA20.gpio import gpio, port
gpio.init()

# цифры-разряды наших часов, моделирует лампы устройства. Всего 6 ламп: ЧЧ ММ СС
digits = [0]*6
# таблица двоичных чисел для декодера:
encoded = ['0000', '0001', '0010', '0011', '0100', '0101', '0110', '0111', '1000', '1001']
# таблица GPIO контактов декодера
decoder_ports = [port.PC0, port.PC1, port.PC2, port.PC3]
# таблица GPIO контактов ламп
lamps_ports = [port.PA19, port.PA7, port.PA8, port.PA9, port.PA10, port.PA20]
# инициализируем эти порты на выход сигнала
for p in decoder_ports:
    gpio.setcfg(p, gpio.OUTPUT)
for p in lamps_ports:
    gpio.setcfg(p, gpio.OUTPUT)


def set_digit(lamp, value):
    """switch on digit through GPIO"""
    # вначале потушим лампу, которая сейчас горит:
    previous_lamp = 5 if lamp == 0 else lamp - 1
    gpio.output(lamps_ports[previous_lamp], 0)
    # теперь зажжем нужную
    gpio.output(lamps_ports[lamp], 1)
    send_value_to_decoder(value)


def send_value_to_decoder(number):
    """кодирует цифру 0-9 в 4-битное число и посылает его на GPIO 7-10
    Соответствие: разряд_числа -> GPIO:  0->7 1->8 2->9 3->10 """
    code = encoded[number]
    for d in range(4):
        gpio.output(decoder_ports[d], int(code[d]))


if __name__=='__main__':
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