import machine
import ssd1306
import socket
i2c = machine.I2C(-1, machine.Pin(5), machine.Pin(4))
oled = ssd1306.SSD1306_I2C(128, 32, i2c)

settime = (2018, 9, 26, 1, 1, 1, 50, 1)
rtc = machine.RTC()
rtc.datetime(settime)


def do_connect():
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(b"iPhone (63)","12345678")
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())
do_connect()


addr = socket.getaddrinfo('0.0.0.0', 8088)[0][-1]
s = socket.socket()
s.settimeout(0.5)

try:
    s.bind(addr)
except:
    print("An exception occurred")

s.listen(1)

def get_text(s):
    for k, c in enumerate(s):
        text = ''
        if c == '=':
            i = k + 1
            while s[i] != " ":
                if s[i] == "+":
                    text += ' '
                else:
                    text += s[i]
                i += 1
            break
    return text

text = ""

while True:
    oled.fill(0)
    flag = False
    
    try:
        cl, addr = s.accept()
    except :
        pass
    
    try:
        cl_file = cl.makefile('rwb', 0)
        content = cl.recv(1024).decode("utf-8")
        text = get_text(content)
        while True:
            line = cl_file.readline()
            if not line or line == b'\r\n':
                break
        cl.close()
        print(text)
    except:
        pass

    oled.text(text, 0, 20)
    displaytime = rtc.datetime()
    oled.text(
              str(displaytime[0]) + '/' + str(displaytime[1]) + '/' + str(displaytime[2]) + 'Week:' + str(displaytime[3]), 0,
              0)
oled.text(str(displaytime[4]) + ':' + str(displaytime[5]) + ':' + str(displaytime[6]), 0, 10)

oled.show()


