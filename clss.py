from machine import PWM, Pin

# Pico pin classes ala Make
class Led(PWM):
    
    def __init__(self, id:int, name:str='none', freq:int=2000, duty:int=500):
        self.pin = Pin(id)
        self.conf = [freq, duty]
        self.name = name
        self.state = False
        super().__init__(self.pin)
        
    def value(self, val:bool):
        if val and not self.state:
            self.state = True
            self.freq(self.conf[0])
            self.duty_u16(self.conf[1])
        elif self.state:
            self.state = False
            self.conf = [self.freq(), self.duty_u16()]
            self.freq(2000)
            self.duty_u16(0)
            
    def toggle(self):
        self.value(False) if self.state else self.value(True)
        
class Btn(Pin):
    
    def __init__(self, id, pull=Pin.PULL_UP):
        self.state = False
        super().__init__(id, Pin.IN, Pin.PULL_UP)
            
    def pulseCheck(self):
        if self.value() == 0 and not self.state:
            self.state = True
            return True
        elif self.value() == 1:
            self.state = False