from machine import *
from machine import Pin, I2C
import machine
import ssd1306
import time
import utime


switchA = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_UP)
switchB = machine.Pin(13, machine.Pin.IN, value = 0)
switchC = machine.Pin(2, machine.Pin.IN, machine.Pin.PULL_UP)
point = 0
settime = (2018, 12, 1, 1, 1, 1, 1, 1)

def switchAcallback(p):
    global point
    time.sleep(0.1)
    if p.value() == 1:
        point = point + 1
        if(point > 7):
            point = 0

def switchBcallback(p):
    time.sleep(0.1)
    global displaytime
    global point
    print('in')
    temp = list(displaytime)
    temp[point] += 1
    rtc.datetime(temp)
    print('set')


def switchCcallback(p):
    time.sleep(0.1)
    global displaytime
    global point
    temp = list(displaytime)
    temp[point] -= 1
    rtc.datetime(temp)



switchA.irq(trigger=machine.Pin.IRQ_RISING, handler=switchAcallback)
switchB.irq(trigger=machine.Pin.IRQ_RISING, handler=switchBcallback)
switchC.irq(trigger=machine.Pin.IRQ_RISING, handler=switchCcallback)



i2c = machine.I2C(-1, machine.Pin(5), machine.Pin(4))
oled = ssd1306.SSD1306_I2C(128, 32, i2c)

rtc = RTC()
rtc.datetime(settime)



while 1:
    oled.fill(0)
    displaytime = rtc.datetime()
    oled.text(str(displaytime[0]) + '/' + str(displaytime[1]) + '/' + str(displaytime[2]) + 'Week:' + str(displaytime[3]), 0, 0)
    oled.text(str(displaytime[4]) + ':' + str(displaytime[5]) + ':' + str(displaytime[6]), 0, 10)
    oled.show()
