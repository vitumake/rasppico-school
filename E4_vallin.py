from clss import Btn, Led
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

# Quick fix for the display class because its written badly
class DispFix(SSD1306_I2C):
    def __init__(self, width, height, i2c, addr=60, external_vcc=False):
        super().__init__(width, height, i2c, addr, external_vcc)
    
    # Idk why but the normal rect method is fucked somehow so we override it
    # Also added a fill arg because its just better
    def rect(self, x1: int, y1: int, x2: int, y2: int, c: int, f: bool) -> None:
        self.line(x1, y1, x1, y2, c) # Vertical
        self.line(x2, y1, x2, y2, c)
        self.line(x1, y1, x2, y1, c) # Horizontal
        self.line(x1, y2, x2, y2, c)
        
        # If rect is to be filled then fill dat shit
        if f:
            i = y1
            while not i == y2:
                i += 1
                self.line(x1, i, x2, i, c)

# Main menu class
class MainM():
    def __init__(self, disp: DispFix, items:list) -> None:
        self.disp = disp
        self.items = []
        self.slctn = 0 # Index of item
        
        # Values for menu graphics
        self.gap = 3
        offset = 0
        itemHeight = round(self.disp.height/len(items))
        
        # Create menu item list
        for item in items:
            self.items.append((item, (offset+self.gap, offset+itemHeight)))
            offset += itemHeight
        
        # Draw menu
        self.show()
    
    def show(self):
        # Render menu on screen
        self.disp.fill(0)
        
        # Draw led names
        for item in self.items:
            self.disp.text(item[0][0], round(self.disp.width/2-12), item[1][0]+(round(self.disp.height/len(items)/4)), 1)
        self.drawSelection(1)
        self.disp.show() 
        
    def drawSelection(self, f):
        self.disp.rect(self.gap, self.items[self.slctn][1][0], self.disp.width-self.gap, self.items[self.slctn][1][1], f, False)
        self.disp.show()
        
    def select(self, val):
        slctn = self.slctn + val
        if slctn < len(self.items) and not slctn < 0:
            self.drawSelection(0)
            self.slctn = slctn
            self.drawSelection(1)
            
    def selection(self):
        return self.items[self.slctn]

# Settings menu class
class SetM():
    def __init__(self, disp: DispFix, maxVal) -> None:
        self.disp = disp
        self.max = maxVal

        # Screen middle
        self.deltaX = round(self.disp.width/2)
        self.deltaY = round(self.disp.height/2)
        
    def show(self, led: Led):
        
        # Progress value
        self.prog = round(self.max/led.duty_u16()*100) if led.duty_u16() != 0 else 1
        
        # Clear screen
        self.disp.fill(0)
        
        # Print led name
        self.disp.text(led.name, self.deltaX-12, self.deltaY-15, 1)
        
        # Bar border
        self.disp.rect(12, self.deltaY+10, 116, self.deltaY+20, 1, False)

        # Draw bar
        self.showBar()
        
        self.disp.show()
        
    def showBar(self):
        # Draw bar
        self.disp.rect(14, self.deltaY+12, self.prog+14, self.deltaY+18, 1, True)
        self.disp.rect(self.prog+14, self.deltaY+12, 114, self.deltaY+18, 0, True)
        
    def update(self, led: Led, val: int):
        self.prog += val
        if self.prog > 100: self.prog = 100
        elif self.prog < 0: self.prog = 0
        led.duty_u16(round(self.prog/100*self.max))
        self.showBar()
        self.disp.show()
        
# Display
i2c = I2C(1, sda=Pin(14), scl=Pin(15))
disp = DispFix(128, 64, i2c)

# Init leds and put them in the menu items list
leds = [Led(20+i, 'Led' + str(i+1)) for i in range(3)]
items = [(led.name, led) for led in leds]

# Menu classes
mainM = MainM(disp, items)
setM = SetM(disp, 10000)

# Rot pins
btn = Btn(12) # Rot button
dire = Pin(10, Pin.IN, Pin.PULL_UP)
step = Pin(11, Pin.IN, Pin.PULL_UP)

# Rot last state
prevStep = step.value()

# Menu state
Menu = 0

# Main loop
while True:
    
    # Rotary handler
    if prevStep != step.value():
        if not step.value():
            if not dire.value():
                mainM.select(-1) if Menu == 0 else setM.update(mainM.selection()[0][1], 7)
            else:
                mainM.select(1) if Menu == 0 else setM.update(mainM.selection()[0][1], -7)
    prevStep = step.value()
    
    # Rotary btn handler
    if btn.pulseCheck():
        if Menu == 0: 
            Menu = 1
            setM.show(mainM.selection()[0][1])
        else: 
            Menu = 0
            mainM.show()