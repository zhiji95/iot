import machine
import time
led1 = machine.Pin(0, machine.Pin.OUT)
led2 = machine.Pin(2, machine.Pin.OUT)
f1, f2 = 1, 3
counter = 0
while (1):
    counter += 1
    blink = []
    if counter % f1 == 0:
        blink.append(led1)
    if counter % f2 == 0:
        blink.append(led2)
    for led in blink:
        led.value(0)
    time.sleep(0.5)
    for led in blink:
        led.value(1)
    time.sleep(0.5)