import machine
import ssd1306
import socket
i2c = machine.I2C(-1, machine.Pin(5), machine.Pin(4))
oled = ssd1306.SSD1306_I2C(128, 32, i2c)

settime = (2018, 9, 26, 1, 1, 1, 50, 1)
rtc = machine.RTC()
rtc.datetime(settime)


html = """<!DOCTYPE html>
    <html>
    <head> <title>ESP8266 Pins</title> </head>
    <body> <h1>ESP8266 Pins</h1>
    <table border="1"> <tr><th>Pin</th><th>Value</th></tr> %s </table>
    </body>
    </html>
    """

def do_connect():
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        #wlan.connect(b"iPhone (63)","12345678")
        wlan.connect(b"sun", "12345678")
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())
do_connect()


addr = socket.getaddrinfo('0.0.0.0', 8088)[0][-1]
s = socket.socket()


try:
    s.bind(addr)
except:
    print("An exception occurred")

s.listen(10)
s.settimeout(0.5)

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

text_l = []
text = ""
flag1 = 0;
while True:
    oled.fill(0)
    
    
    try:
        cl, addr = s.accept()
        # cl_file = cl.makefile('rwb', 0)
        content = cl.recv(1024).decode("utf-8")
        text = get_text(content)
        if text in text_l:
            text = text_l[-1]
        else:
            text_l.append(text)
        # while True:
        #     line = cl_file.readline()
        #     if not line or line == b'\r\n':
        #         break
        cl.close()
        print(text)
    except:
        pass
    
    if text[0:7] == 'turn on' and flag1 == 1:
        oled = ssd1306.SSD1306_I2C(128, 32, i2c)
        print("i am in turn on")
        flag1 = 0
    if text[0:8] == 'turn off' and flag1 == 0:
        oled.poweroff()
        print("i am in turn off")
        flag1 = 1

    oled.text(text, 0, 20)
    displaytime = rtc.datetime()
    oled.text(
              str(displaytime[0]) + '/' + str(displaytime[1]) + '/' + str(displaytime[2]) + 'Week:' + str(displaytime[3]), 0,
              0)
oled.text(str(displaytime[4]) + ':' + str(displaytime[5]) + ':' + str(displaytime[6]), 0, 10)
oled.show()



