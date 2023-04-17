from machine import Pin, I2C, ADC, Timer, PWM
import utime
#from ssd1306 import SSD1306_I2C
import micropython
micropython.alloc_emergency_exception_buf(250)

def toggle_pin(tid):
    global adc_val
    adc_val = adc_count.read_u16()

adc_count = ADC(26) 
dig = Pin(27, Pin.IN)
adc_val = 0
adc_volts = 0     
tmr = Timer(freq = 10, callback = toggle_pin)
#i2c = I2C(1, sda= Pin(14), scl = Pin(15), freq = 400000)
#oled = SSD1306_I2C(128, 64, i2c)

# dig.value(0);

while True:
    adc_volts = (adc_val/65534)*3.3
    print(f'Digital {dig.value()}')
    # print("ADC Count: " + str(adc_val))
    print("ADC volts: " + str(adc_volts))
    utime.sleep(0.1)