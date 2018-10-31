import socket
import json
from sklearn import preprocessing
from sklearn.externals import joblib
import numpy as np
import sys
import decision_tree
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
            print(a)
            print(type(a))
            res = lambda_handler(json.loads(a.decode()),[])
            conn.sendall(json.dumps(res).encode())
    return data

        
def lambda_handler(event, context):
    '''

    :param event:
    :param context:
    :return:
    '''
    global labels
    '''Use decision tree'''
    x = event['content']['data']['x']
    dt = decision_tree(x, x)
    return {
        "statusCode": 200,
        "body": dt.fit()
    }
    '''use svm'''
    '''
    clf = joblib.load('gesture.joblib')
    x = event['content']['data']['x']
    y = event['content']['data']['y']
    dt = decision_tree(x, x)
    features = x + y
    features = np.array([features])
    res = clf.predict(features)
    return {
        "statusCode": 200,
        "body": int(res[0])
    }
    '''

listen()