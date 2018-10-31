import numpy as np

class decision_tree:
    def __init__(self, x, y, prune=False, model1=None, model2=None):
        '''
        :param x: input data on x axis
        :param y: input data on y axis
        :param prune: whether prune all starting and ending zeros
                    (Slow motion data are suggested no to do so)
        :param model1: the model for c, u classification
        :param model2: the model for a, b classification
        '''
        assert type(x) == list
        assert type(y) == list
        self.features = x + y
        self.x = x
        self.y = y
        self.prune = prune
        i = 0
        if prune:
            self.x_prune = []
            self.y_prune = []
            while x[i] == 0 and y[i] == 0:
                i += 1
            while i < len(x):
                self.x_prune.append(x[i])
                self.y_prune.append(y[i])
                i += 1
            j = -1
            while x[j] == 0 and y[j] == 0:
                self.x_prune.pop()
                self.y_prune.pop()
                j -= 1
                if -j > len(self.x_prune):
                    break
            self.features_prune = self.x_prune + self.y_prune
        self.label = ['c', 'o', 'l', 'u', 'm', 'b', 'i', 'a']
        self.model1 = model1
        self.model2 = model2

    def fit(self):
        if self.prune:
            l = len(self.x_prune)
        else:
            l = len(self.x)
        if l >= 80:
            return 1
        elif l < 15:
            return 6
        elif l < 30:
            return 2
        elif l < 45:
            #             index = self.model1.predict(self.x_prune[:20]+self.y_prune[:20])
            index = np.random.randint(2)
            return [0, 3][index]
        elif l < 60:
            #             index = self.model2.predict(self.x_prune[:30]+self.y_prune[:30])
            index = np.random.randint(2)
            return [7, 5][index]
        else:
            return 4
