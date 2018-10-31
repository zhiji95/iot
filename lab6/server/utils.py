import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn import preprocessing
from sklearn.model_selection import GridSearchCV
#from sklearn.grid_search import GridSearchCV
from sklearn.metrics import accuracy_score,make_scorer
from sklearn.svm import SVC


def sampling(l, n):
    '''
    Sampling all sequence into length of n so that ensures all inputs have same amount of features.
    '''
#     sample sequence l into a sequence with length of n
    result = []
    for i in range(n):
        result.append(l[int((i/n)*len(l))])
    return result
def normalize(x):
    '''
    Normalize x.
    '''
    scaler = preprocessing.StandardScaler().fit(x)
    X_nomalized = scaler.transform(x)
    return X_nomalized
def svm():
    '''
    Relatively good svm model gridsearch. Basically the same as mnist model.
    '''
    
    # Set the parameters by cross-validation  
    tuned_parameters = {'kernel': ['rbf'], 'gamma': [0.01,0.05,0.1,0.5],  'C': [0.1,0.5,1,5]}
    clf = GridSearchCV(SVC(), tuned_parameters, cv = 5,
                       scoring = 'accuracy')
    print(clf)
    return clf
def svm_bad():
    '''
    Bad svm model but should be good for large datasets.
    '''
    gammas, Cs = [], []
    for a in np.r_[-15: 4][::2]:
        gamma = pow(float(2), a)
        gammas.append(gamma)
    for b in np.r_[-5: 16][::2]:
        c = pow(float(2), b)
        Cs.append(c)
        # Set the parameters by cross-validation  
        tuned_parameters = {'kernel': ['rbf'], 'gamma': gammas,  'C': Cs}
        clf = GridSearchCV(SVC(), tuned_parameters, cv = 5,
                      scoring = 'accuracy')
        return clf