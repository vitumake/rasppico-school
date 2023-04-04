from clss import Led, Btn
from time import sleep_ms
from machine import I2C, Pin
from ssd1306 import SSD1306_I2C

# display
i2c = I2C(1, sda=Pin(14), scl=Pin(15))
disp = SSD1306_I2C(128, 64, i2c)



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
        