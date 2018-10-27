import machine
from machine import *
import ssd1306
import time
import socket
import urequests as requests
import json


def do_connect():
    import network
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        if not wlan.isconnected():
            print('connecting to network...')
            wlan.connect(b'Columbia University')
            while not wlan.isconnected():
                pass
                    print('network config:', wlan.ifconfig())


urllocation = "https://0hzikyemyj.execute-api.us-east-2.amazonaws.com/default/4764"


def http_post(url, d):
    r = requests.post(url, data=json.dumps(d))
    return r.json()


switchA = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_UP)
flag = 0

data = {}
xdata = []
ydata = []
zdata = []
n = 0

def switchAcallback(p):
    print("i am in callback")
    global flag
    global xdata
    global ydata
    global zdata
    global n
    time.sleep(0.1)
    if p.value() == 1:
        print("in _______")
        flag = 1 if flag == 0 else 0
            if flag == 0:
                n += 1
                    l = {
                        "label": "o",
                            "n": n,
                                "number": len(xdata),
                                "content": {
                                    "data": {
                                        "x": xdata,
                                            "y": ydata,
                                                "z": zdata
                                                }
                                                }
                                                    
                                                    }
                                                        do_connect()
                                                        http_post(urllocation, l)
                                                        print("send success")
                                                        xdata, ydata, zdata = [], [], []




switchA.irq(trigger=machine.Pin.IRQ_RISING, handler=switchAcallback)

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

def dp(d):
    return 128-abs(128-d)


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
    
    # x = test2[0] +test2[1]*256 # if test2[1] <128 else test2[1] - 255
    # y = test4[0] + test4[1]*256 # if test4[1] <128 else test4[1] - 255
    # z = test6[0] + test6[1]*256 # if test6[1] <128 else test6[1] - 255
    x = dp(test1[1]) +dp(test2[1])*256 # if test2[1] <128 else test2[1] - 255
    y = dp(test3[1]) + dp(test4[1])*256 # if test4[1] <128 else test4[1] - 255
    z = dp(test5[1]) + dp(test6[1])*256 # if test6[1] <128 else test6[1] - 255
    print(x, y, z)
    
    if (flag):
        xdata.append(x)
        ydata.append(y)
        zdata.append(z)
    
    oled.fill(0)
    displaytime = rtc.datetime()
    oled.show()

