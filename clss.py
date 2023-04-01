from machine import PWM, Pin

class Led(PWM):
    
    def __init__(self, id:int, freq:int=2000, duty:int=500):
        self.pin = Pin(id, Pin.OUT)
        self.conf = [freq, duty]
        self.state:bool = False
        super().__init__(self.pin)
        
    def freq(self, freq: int = ...):
        self.conf = [freq, self.conf[1]]
        return super().freq(freq)
        
    def duty_ns(self, dur: int= ...):
        self.conf = [self.conf[0], dur]
        return super().duty_ns(dur)
        
    def value(self, val:bool):
        if not val:
            self.conf = [self.freq(), self.duty_ns()]
            self.state = False
            self.freq(2000)
            self.duty_ns(0)
        else:
            self.state = True
            self.freq(self.conf[0])
            self.duty_ns(self.conf[1])
    
    def toggle(self):
        self.value(False) if self.state else self.value(True)