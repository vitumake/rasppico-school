import math, time, machine

led = machine.Pin(20)
pwmLed = machine.PWM(led)

#pwmLed.freq(500)
#pwmLed.duty_u16(312)

def ledOn():
    for i in range(20):
        pwmLed.duty_u16(int((i/10)**2)*500+500)
        time.sleep_ms(10)
        
def ledOff():
    for i in range(20):
        pwmLed.duty_u16(int(((i/10)**2)*-1)*500+500)
        time.sleep_ms(10)