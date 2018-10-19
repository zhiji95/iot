import machine
import time
#alocate the pin for both led and vibrator
pinled = machine.Pin(12)
pinvib = machine.Pin(13)
#set pwm for inputs of led and vibrator
pwmled = machine.PWM(pinled)
pwmvib = machine.PWM(pinvib)
#set the pwm frequencies for both led and vibrator
pwmled.freq(300)
pwmvib.duty(0)
#define the input from light sensor
adc = machine.ADC(0)
#set the input of the switch and let it be zero when disconnected
swinr = machine.Pin(15, machine.Pin.IN)
swind = machine.Pin(4, machine.Pin.IN)
led = machine.Pin(2, machine.Pin.OUT)
led.value(1)

t = True
def swchange(p):
    global t
    time.sleep(0.1)
    led.value(0)
    if p.value() == 1:
        t = False
    else:
        t = True

def swchange1(p):
    global t
    led.value(0)
    time.sleep(0.1)
    if p.value() == 0:
        t = True
    else:
        t = False


swinr.irq(trigger=machine.Pin.IRQ_RISING, handler=swchange)
swind.irq(trigger=machine.Pin.IRQ_FALLING, handler=swchange1)


while (1):
    if t:
    	i = 0
        pwmvib.duty(0)
    else:
    #reading from light sensor
        i = adc.read()
        pwmvib.duty(1000)
    #change the frequency and the light intensity according to the light sensor input
    pwmled.duty(int(i/3))
    pwmvib.freq(i)
