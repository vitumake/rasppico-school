import urequests as requests 
import network
from time import sleep
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
 
APIKEY = "pbZRUi49X48I56oL1Lq8y8NDjq6rPfzX3AQeNo3a" 
CLIENT_ID = "3pjgjdmamlj759te85icf0lucv" 
CLIENT_SECRET = "111fqsli1eo7mejcrlffbklvftcnfl4keoadrdv1o45vt9pndlef" 
 
LOGIN_URL = "https://kubioscloud.auth.eu-west-1.amazoncognito.com/login" 
TOKEN_URL = "https://kubioscloud.auth.eu-west-1.amazoncognito.com/oauth2/token" 
REDIRECT_URI = "https://analysis.kubioscloud.com/v1/portal/login" 
 
# Display
i2c = I2C(1, sda=Pin(14), scl=Pin(15))
disp = SSD1306_I2C(128, 64, i2c)
 
# Wlan
SSID = 'Ilmanlankaa'
WLANPASS = 'Keppihevonen'
 
def printOled(lines):
    offset = 0
    disp.fill(0)
    for i in lines:
        offset += 10
        disp.text(i[0], i[1], offset)
    disp.show()
 
def connect():
    
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, WLANPASS)
    while wlan.isconnected() == False:
        printOled([('Connecting...', 0)])
        print('Connecting...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    printOled([(f'Connected on {ip}', 0)])
    print(f'Connected on {ip}\n')
    
def postKubios():
    
    printOled([("Waiting for", 8), ('kubios...', 8)])
    
    resp = requests.post(
        url=TOKEN_URL,
        data='grant_type=client_credentials&client_id={}'.format(CLIENT_ID), headers={'Content-Type': 'application/x-www-form-urlencoded'},
        auth=(CLIENT_ID, CLIENT_SECRET))
    resp = resp.json()
    access_token = resp["access_token"]
    
    data_set = {
        "type": "RRI",
        "data": [828, 836, 852, 760, 800, 796, 856, 824, 808, 776, 724, 816, 800, 812, 812, 812, 756, 820, 812, 800],
        "analysis": {
            "type": "readiness"
        }
    }
    
    resp = requests.post(
        url="https://analysis.kubioscloud.com/v2/analytics/analyze",
        headers={"Authorization": "Bearer {}".format(access_token),
                 "X-Api-Key": APIKEY},
        json=data_set)
    resp = resp.json()
    
    if resp['status'] == "ok":
        print("request succesful")
        printOled([("Kubios analysis", 0), ("succesful", 0)])
        sleep(1)
        
        # Draw to screen
        printOled([('Kubios analysis', 8), 
            (f'sns_index: {resp["analysis"]["sns_index"]}', 0), 
            (f'pns_index: {resp["analysis"]["pns_index"]}', 0)
        ])
        
    else:
        print(resp)
        print("Kubios analysis failed")
        resp = None

# Main
connect()
postKubios()