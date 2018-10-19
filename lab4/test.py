import requests
import json

url = "https://api.openweathermap.org/data/2.5/weather?lat=%s&lon=%s&APPID=34ff8085d3b99815d850093dda28e624" % (13.0, 23.0)

r = requests.get(url)
print(r.text)