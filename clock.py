import datetime
from time import sleep
import os

# цифры-разряды наших часов, всего 6 ламп
digits = [0, 0,  # hour
          0, 0,  # minute
          0, 0]  # second

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

        for digit_number, value in enumerate(digits):
            set_digit(digit_number, value)
            sleep(0.0008)
