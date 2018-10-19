import machine
from machine import *
import ssd1306
import time
import urequests as requests
import json

i2c = machine.I2C(-1, machine.Pin(5), machine.Pin(4))
oled = ssd1306.SSD1306_I2C(128, 32, i2c)


def do_connect():
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(b'Columbia University')
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())

l = {
    "homeMobileCountryCode": 310,
    "homeMobileNetworkCode": 410,
    "radioType": "gsm",
    "carrier": "Vodafone",
    "considerIp": "true",
    "cellTowers": [
        {
            "cellId": 42,
            "locationAreaCode": 415,
            "mobileCountryCode": 310,
            "mobileNetworkCode": 410,
            "age": 0,
            "signalStrength": -60,
            "timingAdvance": 15
        }
    ],
    "wifiAccessPoints": [
        {
            "macAddress": "00:25:9c:cf:1c:ac",
            "signalStrength": -43,
            "age": 0,
            "channel": 11,
            "signalToNoiseRatio": 0
        }
    ]
}

urllocation = "https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyDPfh87_FSRl9-WpTmEKuJpx6Bq0uAKUN0"



def http_post(url, d):
    r = requests.post(url, data=json.dumps(d))
    return r.json()


do_connect()
location = http_post(urllocation, l)



lat = location['location']['lat']
lon = location['location']['lng']

urlweather = "https://api.openweathermap.org/data/2.5/weather?lat=%s&lon=%s&APPID=34ff8085d3b99815d850093dda28e624" % (lat, lon)
weather = requests.get(urlweather).json()


oled.text(str(location['location']['lat']) + ',' + str(location['location']['lng']), 0, 0)
oled.text(str(weather['main']['temp']), 0, 10)
oled.text(str(weather['weather'][0]['description']), 0, 20)
oled.show()