import pandas as pd
import numpy as np
import ast
from utils import *
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import normalize
from sklearn import preprocessing
from sklearn.utils import shuffle
from scipy.sparse import coo_matrix
from sklearn.model_selection import train_test_split
from sklearn.externals import joblib


class gesture_recognition:
    ''' 
    The argument of object constructor is the path(filename of the file you stored your data).
    If you would like to get train and test seperatedly, please name your training csv file as 'train.csv',
    and testing csv as 'test.csv'. 
    If your would like to got the recognition result by random split, please name your file as 'all.csv'. 
    and use train_test() function. That will take care of spliting, training and evaluating seperately.
    '''
    def __init__(self, filename):
        assert type(filename) == str
        self.path = './%s/'%(filename)
        self.labels = ['c','o','l','u','m','b','i','a']
        self.scaler = None
    def load_all(self):
        return pd.read_csv(self.path+'4764-15.csv')
    def load_train(self):
        return pd.read_csv(self.path+'train.csv')
    def load_test(self):
        return pd.read_csv(self.path + 'test.csv')
    def get_train(self, sample_rate = 20):
        df = self.load_train()
        X, y = [],[]
        for i, c in enumerate(self.labels):
            df_l = df.loc[df['label (S)'] == c]
            X_l, y_l = self.get_xy(df_l, i, sample_rate)
            X += X_l
            y += y_l
        X_sparse = coo_matrix(X)
        X, X_sparse, y = shuffle(X, X_sparse, y, random_state=0)
        scaler = preprocessing.Normalizer().fit(X)
        X_nomalized = scaler.transform(X)
        self.scaler = scaler
        return np.array(X_nomalized),np.array(y)
    def get_all(self, sample_rate, shaffle = False):
        X, y = [], []
        df = self.load_all()
        for i, c in enumerate(self.labels):
            df_l = df.loc[df['label (S)'] == c]
            X_l, y_l = self.get_xy(df_l, i, sample_rate)
            X += X_l
            y += y_l
        if shuffle:
            X_sparse = coo_matrix(X)
            X, X_sparse, y = shuffle(X, X_sparse, y, random_state=0)
#         X_nomalized  = preprocessing.normalize(X)
        X_train, X_test, y_train, y_test = train_test_split(X , y, test_size = 0.3, stratify = y)
''' We didn't implemnent normalize in on both training and testing end. But in most of machine learning model, 
    the normalization are required and usually improves accuracy. We offers three ways to normalize.
'''
        '''Normalize 1'''
#         X_train = preprocessing.normalize(X_train)
#         X_test = preprocessing.normalize(X_test)
        '''Normalize 2'''
#         scaler = preprocessing.Normalizer().fit(X_train)
#         X_train = scaler.transform(X_train)
#         X_test = scaler.transform(X_test)
        '''Normalize 3'''
#         scaler = preprocessing.StandardScalar().fit(X_train)
#         X_train = scaler.transform(X_train)
#         X_test = scaler.transform(X_test)
#         print(len(X_test[0]))
#         X_test = scaler.transform(X_test)
#         scaler_filename = "scaler.save"
#         joblib.dump(scaler, scaler_filename)
        return X_train, X_test, y_train, y_test
    def train_test(self, model):
        X_train, X_test, y_train, y_test = self.get_all(60)
        model.fit(X_train, y_train)
        joblib.dump(model, 'gesture.joblib')
        training_accuracy = accuracy_score(y_train, model.predict(X_train))
        testing_accuracy = accuracy_score(y_test, model.predict(X_test))
#         print(model.predict(X_test[2]), y_test)
        print("Training accuracy is: ", training_accuracy)
        print("Testing accuracy is: ", testing_accuracy)
        d_train = {"Train prediction is:  ": model.predict(X_train),
             "Groundtruth is: ": y_train
            }
        d_test = {"Train prediction is:  ": model.predict(X_test),
             "Groundtruth is: ": y_test
            }
        df_train = pd.DataFrame(data=d_train)
        df_test = pd.DataFrame(data=d_test)
        return df_train, df_test
            
    def get_test(self, sample_rate = 30):
        df = self.load_test()
        X, y = [],[]
        for i, c in enumerate(self.labels):
            df_l = df.loc[df['label (S)'] == c]
            X_l, y_l = self.get_xy(df_l, i, sample_rate)
            X += X_l
            y += y_l
        X_sparse = coo_matrix(X)
        X, X_sparse, y = shuffle(X, X_sparse, y, random_state=0)
        X_nomalized = self.scaler.transform(X)
        return np.array(X_nomalized),np.array(y)
    def train(self, model = svm(), verbose = False):
        X, y = self.get_train()
#         scaler = preprocessing.Normalizer().fit(X)
#         X_nomalized = scaler.transform(X)
        model.fit(X, y)
        if verbose:
            training_accuracy = accuracy_score(y, model.predict(X))
            print("Training accuracy is: ", training_accuracy)
            d = {"Prediction is:  ": model.predict(X),
                 "Groundtruth is: ": y
                }
            df = pd.DataFrame(data=d)
            print(df)
            return model, df
        return model
    def test(self, model = svm(), verbose = False):
        model, df_train = self.train( model = model, verbose = verbose)
        X, y = self.get_test()
        
        if verbose:
            testing_accuracy = accuracy_score(y, model.predict(X))
            print("Testing accuracy is: ", testing_accuracy)
            d = {"Prediction is:  ": model.predict(X),
                 "Groundtruth is: ": y
                }
            df = pd.DataFrame(data=d)
            
            return testing_accuracy, df
        return testing_accuracy
            
    def get_xy(self, df, label, n = 30):
        features, labels = [], []
        for i in df['content (M)']:
            x = []
            d_x = ast.literal_eval(i)['data']['M']['x']['L']
            for j in range(len(d_x)):
                x.append(int(d_x[j]['N']))
            x = sampling(x, n)
            y = []
            d_y = ast.literal_eval(i)['data']['M']['x']['L']
            for j in range(len(d_y)):
                y.append(int(d_y[j]['N']))
            y = sampling(y,n)
            features.append(x + y)
            labels.append(label)
        return features, labels