from math import floor
import machine, time

led1 = machine.Pin(20, machine.Pin.OUT)
led2 = machine.Pin(21, machine.Pin.OUT)
led3 = machine.Pin(22, machine.Pin.OUT)
led4 = machine.Pin('LED', machine.Pin.OUT)

#Decimal to binary
def binary(num):
    binary = []
    #Range is number of bits to use
    for i in range(3):
        binary.insert(0, num%2)
        num=floor(num/2)
    return binary
        
arr = []

#Construct binary array
for i in range(0, 8):
    arr.append(binary(i))

while True:
    for b in arr:
        led4.value(0)
        time.sleep(1)
        led4.value(1)
        led1.value(b[0])
        led2.value(b[1])
        led3.value(b[2])
        