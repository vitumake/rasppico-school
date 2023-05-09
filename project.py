from fifoClass import Fifo
from piotimer import Piotimer
from machine import ADC
from ssd1306 import SSD1306_I2C
from machine import Pin, I2C
import urequests as requests
import network
import machine
from time import sleep

# network info
ssid = "OnePlus5G"
password = "233224792"


# Connect to WLAN
def connect():
    global ip
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        toDisplayData('Connecting...', 0, 20)
        print('Connecting...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    toDisplayData("Connected!", 0, 20)
    print(f'Connected on {ip}\n')
    sleep(1)


# amount of samples
samples = 20

# interrupt
buttonRot = Pin(12, Pin.IN, Pin.PULL_UP)

# KUBIOS INFO
APIKEY = "pbZRUi49X48I56oL1Lq8y8NDjq6rPfzX3AQeNo3a"
CLIENT_ID = "3pjgjdmamlj759te85icf0lucv"
CLIENT_SECRET = "111fqsli1eo7mejcrlffbklvftcnfl4keoadrdv1o45vt9pndlef"
LOGIN_URL = "https://kubioscloud.auth.eu-west-1.amazoncognito.com/login"
TOKEN_URL = "https://kubioscloud.auth.eu-west-1.amazoncognito.com/oauth2/token"
REDIRECT_URI = "https://analysis.kubioscloud.com/v1/portal/login"


# OLED INFO
i2c = I2C(1, sda=Pin(14), scl=Pin(15))
oled = SSD1306_I2C(width=128, height=64, i2c=i2c)
oled.init_display()

frequency = 250
adc = ADC(0)
values = Fifo(500)

# STORE ADC


def get_sample(ok):
    values.put(adc.read_u16())

# show bpm on oled


def toDisplayPuls(data, x, y):
    oled.fill(0)
    oled.text(f'BPM: {str(data)}', x, y)
    oled.show()

# show some text on oled


def toDisplayData(text, x, y):
    oled.text(text, x, y)
    oled.show()


def startdisplay():
    print("Press the pink button to start")
    oled.fill(0)
    oled.text("Place finger", 0, 0)
    oled.text("on the sensor", 0, 10)
    oled.text("and press", 0, 20)
    oled.text("the pink button", 0, 30)
    oled.text("to start", 0, 40)
    oled.show()

# send data to server
def toServer(data):
    try:
        dataset = {
            "uid": 2,
            "data": data
        }
        response = requests.post(
            url="https://api.kammio.w1de.one/upload",
            headers={'Accept': 'application/json'},
            json=dataset)
        status = response.status_code

        if status != 200:
            print(f'POST error: {status}')
            response = None
        print("server POST status: SUCCESS")
    except Exception as e:
        print(e)
        print("server POST status: FAILED")
        response = None

    return response


tmr = Piotimer(mode=Piotimer.PERIODIC, freq=frequency, callback=get_sample)

# data sent to Kubios
kubiosdata = []


def calculateBPM(data):
    global frequency
    firstPeak = secondPeak = secondValue = None
    maxPeak = 0
    treshold = sorted(data.data)[round(data.size/2)]
    margin = 100

    for i, val in enumerate(data.data):
        if not secondValue:
            if val > maxPeak:
                firstPeak = i
                maxPeak = val
            elif val < treshold - margin and maxPeak > treshold:
                secondValue = True
                maxPeak = 0

        elif val > maxPeak:
            secondPeak = i
            maxPeak = val

    if firstPeak is not None and secondPeak is not None:
        bpm = (secondPeak - firstPeak) * (1 / frequency) * 60
        kubiosdata.append(
            round((int(secondPeak) - int(firstPeak))*(1000/frequency)))
        if bpm < 60 or bpm > 120:
            bpm = bpm
    else:
        bpm = 0

    return int(bpm)



# show kubios data on oled
def toDisplayKubios(response):
    if response != None:
        oled.fill(0)
        oled.text(f'sns: {response["analysis"]["sns_index"]}', 0, 0)
        oled.text(f'pns: {response["analysis"]["pns_index"]}', 0, 20)
        oled.text(
            f'mean bpm: {round(response["analysis"]["mean_hr_bpm"])}', 0, 40)
        oled.show()
        print(f'sns index: {response["analysis"]["sns_index"]}')
        print(f'pns index: {response["analysis"]["pns_index"]}')
        print(f'average BPM: {round(response["analysis"]["mean_hr_bpm"])}')
    else:
        oled.fill(0)
        oled.text("Server error", 0, 0)
        oled.text("Try again later", 0, 20)
        oled.show()


# OPEN KUBIOS SESSION AND GET SNS/PNS INDEXES
def kubios():
    print("getting data from kubios...")
    oled.fill(0)
    oled.text("Analysing data...", 0, 0)
    oled.show()
    response = requests.post(
        url=TOKEN_URL,
        data='grant_type=client_credentials&client_id={}'.format(CLIENT_ID), headers={'Content-Type': 'application/x-www-form-urlencoded'},
        auth=(CLIENT_ID, CLIENT_SECRET))
    response1 = response.json()  # Parse JSON response into a python dictionary
    # Parse access token out of the response dictionary
    access_token = response1["access_token"]
    data_set = {
        "type": "RRI",
        "data": kubiosdata,
        "analysis": {
            "type": "readiness"
        }
    }
    response = requests.post(
        url="https://analysis.kubioscloud.com/v2/analytics/analyze",
        headers={"Authorization": "Bearer {}".format(access_token),
                 "X-Api-Key": APIKEY},
        json=data_set)
    response = response.json()

    status = response['status']

    if status == "ok":
        print("Kubios analysis succesful")
        toDisplayData("Kubios analysis", 0, 10)
        toDisplayData("succesful", 0, 20)
    else:
        print(response)
        print("Kubios analysis failed")
        response = None

    return response


# button state tracker
on = False

# interrupt handler
def turnOn(pin):
    global on
    on = True


# pink button interrupt
buttonRot.irq(handler=turnOn, trigger=Pin.IRQ_FALLING)


def main():
    global samples
    while True:
        if values.full:
            data = calculateBPM(values)
            toDisplayPuls(data, 20, 20)
            if data < 150 and data > 40:
                print(f'BPM: {data}')
            else:
                print("bad sample")
            values.clear()  # clear fifo
            samples -= 1
            if samples <= 0:  # when desired amount of samples is reached
                resp = kubios()  # get kubios analysis
                if resp != None:  # if kubios analysis is successful
                    respServer = toServer(resp)  # send data to raspberry pi server
                    if respServer != None:  # if POST is successful
                        print("database updated!")
                        # notify user that data is uploaded
                        toDisplayData("database updated!", 0, 30)
                    else:  # if POST is unsuccessful
                        print("database update failed!")
                        toDisplayData("database update", 0, 40)
                        toDisplayData("failed !", 0, 50)
                sleep(3)
                toDisplayKubios(resp)  # show kubios analysis on oled
                sleep(1)
                break


# MAIN
try:
    connect()
except KeyboardInterrupt:
    machine.reset()

startdisplay()
sleep(2)

while True:
    if on == True:
        main()
        break