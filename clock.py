import datetime

digits = [0, 0,  # hour
          0, 0,  # minute
          0, 0]  # second

while True:
    time = datetime.datetime.now()
    hour, minute, second = time.hour, time.minute, time.second

    digits[0] = hour // 10
    digits[1] = hour % 10

    digits[2] = minute // 10
    digits[3] = minute % 10

    digits[4] = second // 10
    digits[5] = second % 10

    