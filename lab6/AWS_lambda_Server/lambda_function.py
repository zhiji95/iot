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
