from clss import Led, Btn
from time import sleep_ms
from machine import I2C, Pin

# toggle tuple array
toggles = [
    (Btn(7), Led(20)),
    (Btn(8), Led(21)),
    (Btn(9), Led(22))
    ]


# Interrupt

def off(Pin):
    for i in toggles:
        i[1].value(False)

Btn(12).irq(handler=off, trigger=Pin.IRQ_FALLING)


while True:
        
    # Toggle logic
    for i in toggles:
        if i[0].pulseCheck():
            i[1].toggle()
            
    