from machine import Pin
from time import sleep_ms

led = Pin(20, Pin.OUT)
led1 = Pin(21, Pin.OUT)
led2 = Pin(22, Pin.OUT)

buttonW1 = Pin(9, Pin.IN, Pin.PULL_UP)
buttonW2 = Pin(8, Pin.IN, Pin.PULL_UP)
buttonW3 = Pin(7, Pin.IN, Pin.PULL_UP)
buttonRot = Pin(12, Pin.IN, Pin.PULL_UP)


def offAll(pin):
    led.value(0)
    led1.value(0)
    led2.value(0)


def btnHandler(btn, led):
    while btn.value() == 0:
        sleep_ms(1)
        if btn.value()==1:
            led.toggle()
            break

buttonRot.irq(handler=offAll, trigger=Pin.IRQ_FALLING)

while True:
    btnHandler(buttonW1, led)
    btnHandler(buttonW2, led1)
    btnHandler(buttonW3, led2)