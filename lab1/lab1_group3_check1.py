import machine
import time
led = machine.Pin(0, machine.Pin.OUT)
while (1):
    l = [1,1,1,2,2,2,1,1,1]
    for t in l:
        led.value(0)
        time.sleep(0.5 * t)
        led.value(1)
        time.sleep(0.5)