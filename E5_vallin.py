from clss import Btn
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import math

# Display
i2c = I2C(1, sda=Pin(14), scl=Pin(15))
disp = SSD1306_I2C(128, 64, i2c)

# Toggle btn
btn = Btn(12)

# Sets
setOne = ('Set 1', [1000, 1100, 1000, 1100, 1000, 1100, 1000, 1100, 1000, 1100, 1000, 1100, 
1000, 1100, 1000, 1100, 1000, 1100, 1000, 1100])
setTwo = ('Set 2', [828, 836, 852, 760, 800, 796, 856, 824, 808, 776, 724, 816, 800, 812, 812, 
812, 756, 820, 812, 800])

# Current set
curSet = setOne

# Calculate vals and draw them
def showVals(set):
    
    # Clear screen
    disp.fill(0)
    
    # Values
    meanPPI = round(sum(set[1])/len(set[1]))
    hr = [1/i*1000*60 for i in set[1]]
    meanHR = round(sum(hr)/len(hr))
    sdnn = round(math.sqrt(sum([(i-meanPPI)**2 for i in set[1]])/(len(set[1])-1)))
    rmssd = round(math.sqrt(sum([(set[1][i-1]-set[1][i])**2 for i in range(len(set[1]))])/(len(set[1])-1)))
    
    disp.text(set[0], 50, 10)
    disp.text(f'mean PPI: {meanPPI}ms', 2, 20)
    disp.text(f'mean HR: {meanHR}bpm', 2, 30)
    disp.text(f'sdnn: {sdnn}ms', 2, 40)
    disp.text(f'rmssd: {rmssd}ms', 2, 50)
    disp.show()

# Draw to screen
showVals(curSet)
    
while True:
    if btn.pulseCheck():
        curSet = setOne if curSet == setTwo else setTwo
        showVals(curSet)