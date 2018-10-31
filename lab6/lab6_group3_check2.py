import machine
import ssd1306
import socket
import time
import json

i2c = machine.I2C(-1, machine.Pin(5), machine.Pin(4))
oled = ssd1306.SSD1306_I2C(128, 32, i2c)
setalarm = [2018, 9, 26, 1, 1, 2, 0, 0]
rtc = machine.RTC()
rtc.datetime((2018, 9, 26, 1, 1, 1, 50, 1))
text = ""
adc = machine.ADC(0)


point = 0
xdata=[]
flag = 0
send = False
labels = ['c', 'o', 'l', 'u', 'm', 'b', 'i', 'a','null']
addr = socket.getaddrinfo('0.0.0.0', 8088)[0][-1]
s = socket.socket()
gesture = False

def sendData(flag, content):
    global label
    global xdata
    print(content)
    if flag == 0:
        label = 'weather'
    elif flag == 1:
        label = 'twitter'
    else:
        label = 'null'
    ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ss.connect(('18.220.181.241', 8080))
    l = {
        "label": label,
        "n": 0,
        "number": len(xdata),
        "content": {
            "data": {
                "x": xdata,
                "content": content
            }
        }

    }
    l = json.dumps(l).encode()
    ss.sendall(l)
    data = ss.recv(1024)
    print(type(data),data)
    data = json.loads(data.decode())
    xdata = []
    return data

def do_connect():
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        # wlan.connect(b"iPhone (63)", "12345678")
        wlan.connect(b"sun", "12345678")
        # wlan.connect(b'MySpectrumWiFid3-2G', "quickacre108")
        # wlan.connect(b"sun", "12345678")
        # wlan.connect(b'Columbia University')
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())



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


def switchAgesture(p):
    global flag
    time.sleep(0.1)
    if p.value() == 1:
        flag = 1


def switchCgesture(p):
    global send
    if p.value() == 1:
        send = True

do_connect()
def dp(d):
    if (d > 128):
        return d - 255
    return d





try:
    s.bind(addr)
except:
    print("An exception occurred")

s.listen(1)
s.settimeout(0.1)

def get_text(s):
    for k, c in enumerate(s):
        text = ''
        if c == '=':
            i = k + 1
            while i < len(s) and s[i] != " ":
                if s[i] == "+":
                    text += ' '
                else:
                    text += s[i]
                i += 1
            break
    return text

switchA = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_UP)
switchB = machine.Pin(13, machine.Pin.IN, value=0)
switchC = machine.Pin(2, machine.Pin.IN, machine.Pin.PULL_UP)
switchA.irq(trigger=machine.Pin.IRQ_RISING, handler=switchAcallback)
switchB.irq(trigger=machine.Pin.IRQ_RISING, handler=switchBcallback)
switchC.irq(trigger=machine.Pin.IRQ_RISING, handler=switchCcallback)
spi = machine.SPI(1, baudrate=2000000, polarity=1, phase=1)
cs = machine.Pin(15, machine.Pin.OUT)
cs.value(0)
spi.write(b'\x2d')
spi.write(b'\x2b')
cs.value(1)
cs.value(0)
spi.write(b'\x31')
spi.write(b'\x0f')
cs.value(1)
while True:
    oled.fill(0)
    try:
        cl, addr = s.accept()
    except OSError:
        pass
    else:
        content = cl.recv(1024).decode("utf-8")
        text = get_text(content)
        print(text)
        res = 0
        if text[0:7] == 'turn on':
            oled = ssd1306.SSD1306_I2C(128, 32, i2c)
            print("i am in turn on")
            res = 1

        elif text[0:8] == 'turn off':
            oled.poweroff()
            print("i am in turn off")
            res = 2
        elif text[0: len('weather')] == 'weather':
            text = sendData(0, "")['body']
            res = 3
            print(text)

        elif text[0: len('post')] == 'post':
            print("sending twitter")
            text = sendData(1,text[len('post'):])
            text = 'post'
            res = 4
        elif text == 'switch':
            gesture = True
            switchA.irq(trigger=machine.Pin.IRQ_RISING, handler=switchAgesture)
            switchC.irq(trigger=machine.Pin.IRQ_RISING, handler=switchCgesture)
        elif text == 'alarm':
            gesture = False
            switchA.irq(trigger=machine.Pin.IRQ_RISING, handler=switchAcallback)
            switchB.irq(trigger=machine.Pin.IRQ_RISING, handler=switchBcallback)
            switchC.irq(trigger=machine.Pin.IRQ_RISING, handler=switchCcallback)

        response = "HTTP/1.1 200 OK\n" + "Content-Type: text/html\n" + "\n" + "<html><body>Bingo</body></html>\n"
        cl.send(str.encode(response))
        cl.close()
    if gesture:
        x = 0
        y = 0
        sendstatus = "null"
        if (flag):
            cs.value(0)
            test2 = spi.read(5, 0xf3)
            cs.value(1)
            x = dp(test2[1])
            xdata.append(x)
            sendstatus = "collect" + str(len(xdata)) + ' ' + ' ' + str(x)
            if send:
                word = sendData(2,"")
                flag = 0
                send = False
                text = labels[word['body']] + "   success"
    oled.text(text, 0, 20)
    displaytime = rtc.datetime()
    oled.text(
        str(displaytime[0]) + '/' + str(displaytime[1]) + '/' + str(displaytime[2]) + 'Week:' + str(displaytime[3]), 0,
        0)
    oled.text(str(displaytime[4]) + ':' + str(displaytime[5]) + ':' + str(displaytime[6]), 0, 10)
    oled.text(str(setalarm[4]) + ':' + str(setalarm[5]) + ':' + str(setalarm[6]), 64, 10)
    oled.show()

    i = adc.read()

    oled.contrast(int(i / 4))

    if displaytime[4] == setalarm[4] and displaytime[5] == setalarm[5] and displaytime[6] == setalarm[6]:
        oled.fill(1)
        oled.show()




