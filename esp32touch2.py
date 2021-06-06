import machine
import utime

touch7 = machine.TouchPad(machine.Pin(27))

lowvalue = 1000
loopit = True
while loopit:
    touchvalue = touch7.read()
    # print(touchvalue)
    if touchvalue < lowvalue:
        lowvalue=touchvalue
        print('LowValue = {0}'.format(lowvalue))
        if lowvalue < 90:
            loopit = False
    utime.sleep_ms(100)
    