import socket
import json
from sklearn import preprocessing
from sklearn.externals import joblib
import numpy as np
import sys
import requests

data = []
labels = ['c', 'o', 'l', 'u', 'm', 'b', 'i', 'a','null']

class decision_tree:
    def __init__(self, x, y, model1 = None, model2 = None):
        assert type(x) == list
        assert type(y) == list
        self.features = x + y
        self.x = x
        self.y = y
        self.label = ['c','o','l','u','m','b','i','a']
    
    def fit(self):
        l = len(self.x)
        lp = len(self.x)
        if l >= 80:
            return 1
        elif lp < 15:
            return 6
        elif lp < 30:
            return 2
        elif lp < 45:
            #             index = self.model1.predict(self.x_prune[:20]+self.y_prune[:20])
            index = np.random.randint(2)
            return [0, 3][index]
        elif lp < 60:
            #             index = self.model2.predict(self.x_prune[:30]+self.y_prune[:30])
            index = np.random.randint(2)
            return [7, 5][index]
        else:
            return 4

def listen():
    global data
    HOST = ''                 # Symbolic name meaning all available interfaces
    PORT = 8080              # Arbitrary non-privileged port
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except OSError as msg:
        s = None
    if s is None:
        print('could not open socket')
        sys.exit(1)
    
    try:
        s.bind((HOST, PORT))
    except:
        print('could not open socket')
    s.listen(1)
    
    while (1):
        conn, addr = s.accept()
        print('Connected by', addr)
        with conn:
            a = conn.recv(4096)
            res = lambda_handler(json.loads(a.decode()),[])
            conn.sendall(json.dumps(res).encode())
    return data

def http_post(url, d):
    r = requests.post(url, data=json.dumps(d))
    return r.json()

def post_twitter(twitter_posts):
    urltwitter = "https://api.thingspeak.com/apps/thingtweet/1/statuses/update?api_key=%s&status=%s" % (
                                                                                                        "QX56TMCE80SAVU07", twitter_posts)
                                                                                                        twitter = requests.get(urltwitter)
                                                                                                        return twitter.json()

def get_weather():
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
                   
                   urllocation = "https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyCQ5BKGz7wh8LNLYiG1NsLaifhYPI1qLiM"
                   location = http_post(urllocation, l)
                   
                   lat = location['location']['lat']
                   lon = location['location']['lng']
                   urlweather = "https://api.openweathermap.org/data/2.5/weather?lat=%s&lon=%s&APPID=34ff8085d3b99815d850093dda28e624" % (lat, lon)
                   weather = requests.get(urlweather).json()
                   return str(weather['weather'][0]['description'])


def lambda_handler(event, context):
    print(event['label'])
    if (event['label'] == 'twitter'):
        res = post_twitter(event['content']['data']['content'])
    elif (event['label'] == 'weather'):
        res = get_weather()
    else:
        x = event['content']['data']['x']
        print(x)
        res = decision_tree(x, x).fit()
    print(res)
    return {
        "statusCode": 200,
        "body": res
}

listen()
