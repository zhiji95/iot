import machine
from machine import *
import ssd1306
import time


spi = machine.SPI(1, baudrate=2000000, polarity=1, phase=1)

cs = machine.Pin(15, machine.Pin.OUT)  # create and configure in one go


cs.value(0)
spi.write(b'\x2d')
spi.write(b'\x2b')
cs.value(1)
cs.value(0)
spi.write(b'\x31')
spi.write(b'\x0f')
cs.value(1)


settime = (2018, 9, 26, 1, 1, 1, 50, 1)

i2c = machine.I2C(-1, machine.Pin(5), machine.Pin(4))
oled = ssd1306.SSD1306_I2C(128, 32, i2c)

rtc = RTC()
rtc.datetime(settime)

x = 0
y = 10

while True:
    time.sleep(0.01)
    cs.value(0)
    test1 = spi.read(5, 0xf2)
    cs.value(1)


    cs.value(0)
    test2 = spi.read(5, 0xf3)
    cs.value(1)


    cs.value(0)
    test3 = spi.read(5, 0xf4)
    cs.value(1)


    cs.value(0)
    test4 = spi.read(5, 0xf5)
    cs.value(1)


    cs.value(0)
    test5 = spi.read(5, 0xf6)
    cs.value(1)


    cs.value(0)
    test6 = spi.read(5, 0xf7)
    cs.value(1)

    print(test2[1],test4[1],test6[1])

    oled.fill(0)
    displaytime = rtc.datetime()
    ip = 'Hello World'
    oled.text(ip, x, y)
    oled.show()
    if test2[1] > 128:
        x += (256-test2[1])
    if test4[1] > 128:
        y -= (256-test4[1])
    if test2[1] < 128 and test2[1] > 0:
        x -= test2[1]
    if test4[1] < 128 and test4[1] > 0:
        y += test4[1]
    if x < -len(ip) * 8:
        x = 128
    if x > 128:
        x= 0
    if y < 0:
        y = 32
    if y > 32:
        y = 0
