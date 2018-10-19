import machine
import ssd1306
import time

# define the input from light sensor
adc = machine.ADC(0)

pinvib = machine.Pin(12)
pwmvib = machine.PWM(pinvib)
pwmvib.freq(900)
pwmvib.duty(0)

switchA = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_UP)
switchB = machine.Pin(13, machine.Pin.IN, value=0)
switchC = machine.Pin(2, machine.Pin.IN, machine.Pin.PULL_UP)
point = 0
settime = (2018, 9, 26, 1, 1, 1, 50, 1)
setalarm = [2018, 9, 26, 1, 1, 2, 0, 0]


def switchAcallback(p):
    global point
    time.sleep(0.1)
    if p.value() == 1:
        point = point + 1
        if (point > 9):
            point = 0


def switchBcallback(p):
    time.sleep(0.1)
    global displaytime
    global point
    global setalarm
    temp = list(displaytime)
    if point == 7:
        setalarm[4] += 1
    elif point == 8:
        setalarm[5] += 1
    else:
        temp[point] += 1
    rtc.datetime(temp)
    print('set')


def switchCcallback(p):
    time.sleep(0.1)
    global displaytime
    global point
    global setalarm
    temp = list(displaytime)
    if point == 7:
        setalarm[4] -= 1
    elif point == 8:
        setalarm[5] -= 1
    else:
        temp[point] -= 1
    rtc.datetime(temp)


switchA.irq(trigger=machine.Pin.IRQ_RISING, handler=switchAcallback)
switchB.irq(trigger=machine.Pin.IRQ_RISING, handler=switchBcallback)
switchC.irq(trigger=machine.Pin.IRQ_RISING, handler=switchCcallback)

i2c = machine.I2C(-1, machine.Pin(5), machine.Pin(4))
oled = ssd1306.SSD1306_I2C(128, 32, i2c)

rtc = machine.RTC()
rtc.datetime(settime)

counter = 0
counting = False
while 1:
    oled.fill(0)
    displaytime = rtc.datetime()
    oled.text(
        str(displaytime[0]) + '/' + str(displaytime[1]) + '/' + str(displaytime[2]) + 'Week:' + str(displaytime[3]), 0,
        0)
    oled.text(str(displaytime[4]) + ':' + str(displaytime[5]) + ':' + str(displaytime[6]), 0, 10)

    oled.text(str(setalarm[4]) + ':' + str(setalarm[5]) + ':' + str(setalarm[6]), 0, 20)

    oled.show()
    i = adc.read()
    oled.contrast(int(i / 4))

    if displaytime[4] == setalarm[4] and displaytime[5] == setalarm[5] and displaytime[6] == setalarm[6]:
        pwmvib.duty(900)

    if displaytime[4] == setalarm[4] and displaytime[5] == setalarm[5] and displaytime[6] == 5:
        pwmvib.duty(0)
