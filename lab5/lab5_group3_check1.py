import machine
import ssd1306
import socket
i2c = machine.I2C(-1, machine.Pin(5), machine.Pin(4))
oled = ssd1306.SSD1306_I2C(128, 32, i2c)


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


try:
    s.bind(addr)
except:
    print("An exception occurred")

s.listen(1)

def get_text(s):
    # s: input context string
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


while True:
    cl, addr = s.accept()
    print('client connected from', addr)
    cl_file = cl.makefile('rwb', 0)
    content = cl.recv(1024).decode("utf-8")
    text = get_text(content)
    oled.fill(0)
    oled.text("Command:", 0, 0)
    oled.text(text, 0, 10)
    oled.show()
    while True:
        line = cl_file.readline()
        if not line or line == b'\r\n':
            break
    cl.close()
    print(text)
#     break
#rows = ['<tr><td>%s</td><td>%d</td></tr>' % (str(p), p.value()) for p in pins]
#response = html % '\n'.join(rows)
#cl.send(response)


