'''
author: bg
goal: define model interface
type: interface 
refactor: class
'''


'''
Training Handler: Listener for training is completed iff done async
Expectation:
 - notifyTrainingIsCompleted with accuracy level, numper of epocs and duration
'''
class ZModelTrainingHandler():
    def training_completed(self, accuracy_achieved, n_epochs, time_taken): 
        raise NotImplementedError

'''
Expectations:
 - init: Initialize model resources 
 - load: Load model from file 
 - dump: save model to file 
 - accuracy: get accuracy of model 
 - predict: get predicted value for a given observation or set of observations
 - train: train model using given dataset 
 - training_handler: listener for when training is done if done async << TODO: allow multiple listners; one for now
'''

class ZModel():

    
    '''
    '''
    def init(self, name, removeStopWords=True): 
        raise NotImplementedError

    
    '''
    '''
    def load(self, fpath):
        raise NotImplementedError

    '''
    '''
    def dump(self, fpath): 
        raise NotImplementedError

    '''
    '''
    def accuracy(self):
        raise NotImplementedError

    '''
    '''
    def predict(self, observation): 
        raise NotImplementedError
    
    '''
    '''
    def train(self, train_x, train_y, test_x, test_y):
        raise NotImplementedError
    '''
    '''
    def setTrainingHandler(self, training_handler): 
        self.training_handler = training_handler

    '''
    '''
    def updateTrainingHandler(self):
        if self.training_handler is not None:
            self.training_handler.training_completed(self.accuracy, self.training_epochs, self.training_time ) 

    '''
    '''
    def __str__(self):
        return "{} {} with model file '{}'".format( self.__class__, self.name, self.model_fpath)