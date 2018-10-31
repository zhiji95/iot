import machine
import ssd1306
import socket

pins = [machine.Pin(i, machine.Pin.IN) for i in (0, 2, 4, 5, 12, 13, 14, 15)]

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
        #wlan.connect(b"sun", "12345678")
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


text = ""

while True:
    oled.fill(0)
    try:
        cl, addr = s.accept()
    except OSError:
        pass
    else:
        content = cl.recv(1024).decode("utf-8")
        text = get_text(content)
        
        if text[0:7] == 'turn on':
            oled = ssd1306.SSD1306_I2C(128, 32, i2c)
            print("i am in turn on")
            
            response = "HTTP/1.1 200 OK\n" + "Content-Type: text/html\n" + "\n" + "<html><body>Turn on display</body></html>\n"
            cl.send(str.encode(response))
            cl.close()

        elif text[0:8] == 'turn off':
            oled.poweroff()
            print("i am in turn off")
            
            response = "HTTP/1.1 200 OK\n" + "Content-Type: text/html\n" + "\n" + "<html><body>Turn off display</body></html>\n"
            cl.send(str.encode(response))
            cl.close()

else:
    
    response = "HTTP/1.1 200 OK\n" + "Content-Type: text/html\n" + "\n" + "<html><body>Hello World</body></html>\n"
        cl.send(str.encode(response))
        cl.close()

    oled.text(text, 0, 20)
    displaytime = rtc.datetime()
    oled.text(
              str(displaytime[0]) + '/' + str(displaytime[1]) + '/' + str(displaytime[2]) + 'Week:' + str(displaytime[3]), 0,
              0)
oled.text(str(displaytime[4]) + ':' + str(displaytime[5]) + ':' + str(displaytime[6]), 0, 10)
oled.show()
