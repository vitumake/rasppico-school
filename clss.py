from machine import PWM, Pin

# Classes for pico w go board
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
            
# Init array with given size to avoid memory errors.
class samplData:
    def __init__(self, size) -> None:
        self.size = size # Size of array
        self.clear() # Using clear method to init rest of the vars
        
    # Method for pushing data
    def put(self, val):
        if not self.full:
            self.data[self.cursor] = val
            self.datasum += val
            self.cursor += 1
        if self.cursor == self.size: self.full = True
    
    # Method to clear data
    def clear(self):
        self.cursor = 0 # Array cursor for adding data to right place
        self.full = False # Is array full
        self.datasum = 0 # Sum of all values in array
        self.data = [0 for i in range(self.size)]
        
    def average(self):
        return self.datasum/self.cursor+1