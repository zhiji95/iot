import json
from sklearn import preprocessing
from sklearn.externals import joblib
import numpy as np

def lambda_handler(event, context):
    x = event['content']['data']['x']
    y = event['content']['data']['y']
    features = x + y
    features = np.array([features])
    clf = joblib.load('gesture.joblib')
    res = clf.predict(features)
    return {
        "statusCode": 200,
        "body": int(res[0])
    }

event = {
  "label": "o",
  "n": 12,
  "number": 8,
  "content": {
    "data": {
      "x": [0,
  0,
  0,
  0,
  0,
  -9,
  -4,
  -4,
  3,
  8,
  10,
  6,
  2,
  -1,
  -8,
  -4,
  -7,
  -2,
  3,
  9,
  8,
  6,
  4,
  0,
  -3,
  -4,
  -3,
  0,
  0,
  0],
      "y": [0,
  0,
  0,
  0,
  0,
  -4,
  3,
  6,
  7,
  0,
  0,
  -2,
  -5,
  -3,
  -6,
  6,
  2,
  7,
  4,
  2,
  0,
  -3,
  -1,
  -4,
  -2,
  0,
  -1,
  0,
  0,
  0]
    }
  }
}
context = {}
print(lambda_handler(event,context))
