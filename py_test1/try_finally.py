import time

try:
    a = 10 + 10
    time.sleep(2)
    print(a)
except ZeroDivisionError:
    print('제수는 0이 될 수 없습니다!')
try:
    a = 10 / 0
except ZeroDivisionError:
    print('제수는 0이 될 수 없습니다!')
finally:
    print('무조건 실행되는 영역!')