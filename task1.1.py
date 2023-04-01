import machine, time

led1 = machine.Pin(20, machine.Pin.OUT)
led2 = machine.Pin(21, machine.Pin.OUT)
led3 = machine.Pin(22, machine.Pin.OUT)

def ledContr(b1, b2, b3):
    led1.value(b1)
    led2.value(b2)
    led3.value(b3)

#binary array
arr = [
    [0, 0, 0],
    [0, 0, 1],
    [0, 1, 0],
    [1, 0, 0]
    ]

while True:
    for b in arr:
        time.sleep(1)
        ledContr(b[0], b[1], b[2])
        