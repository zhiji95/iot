import socket
import json
from sklearn import preprocessing
from sklearn.externals import joblib
import numpy as np
import sys
import requests
import decision_tree as dt
import SVM

data = []
labels = ['c', 'o', 'l', 'u', 'm', 'b', 'i', 'a','null']

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
    '''

    :param event: The information sent from client end and received on server end.
    :param context: Useless
    :return:
    '''
    print(event['label'])
    if (event['label'] == 'twitter'):
        res = post_twitter(event['content']['data']['content'])
    elif (event['label'] == 'weather'):
        res = get_weather()
    else:
        ''' Decision Tree '''
        x = event['content']['data']['x']
        print(x)
        res = dt(x, x).fit()
        ''' SVM'''
        '''clf = joblib.load('gesture.joblib')
        x = event['content']['data']['x']
        y = event['content']['data']['y']
        dt = dt(x, x)
        features = x + y
        features = np.array([features])
        res = clf.predict(features)'''
    print(res)
    return {
        "statusCode": 200,
        "body": res
    }

listen()