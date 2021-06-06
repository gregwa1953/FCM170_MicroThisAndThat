import machine
import utime

touch7 = machine.TouchPad(machine.Pin(27))

lowvalue = 1000
while True:
    touchvalue = touch7.read()
    # print(touchvalue)
    if touchvalue < lowvalue:
        lowvalue=touchvalue
        print('LowValue = {0}'.format(lowvalue))
    utime.sleep_ms(100)
    