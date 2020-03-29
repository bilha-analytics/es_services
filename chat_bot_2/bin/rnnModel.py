'''
author: bg
goal: NN based Multi-class text classifiers. Retrieval supervised classifier, Retrieval Seq2Seq, Generative 
type: ZModel
refactor: 
'''

import tensorflow as tf
import keras 


import pickle 

import zlogger

import modelz 
from dataSet import lemmatizeTokens

'''

'''
class RetrievalSupervisedNNModel( modelz.ZModel ):

    '''
    setup  RNN layers 
    '''
    def init(self, name, removeStopWords=True): 
        super().init(name) 
        self.model = tf.estimator.DNNClassifier()

    
    '''
    '''
    def accuracy(self):
        raise NotImplementedError

    '''
    '''
    def predict(self, observation):
        raise NotImplementedError

    '''
    Input: 
        train_x : pandas db Vs Gsheet workbook <<< list of rows e.g. at GSheet workbook @ classify phrases
    '''
    def train(self, train_x, train_y=None, test_x=None, test_y=None): 

        def datasetImporter(train_x): 
            featurez_dict = None
            labez_list = None

            return featurez_dict, labez_list 
            
        def featureColumnz(train_x): ## TODO: refactor @ caller or auto decide if numeric or categorical
            featureColumnz = []

            headerz = train_x[0]

            for header in headerz:
                pass 

            return featureColumnz 


        self.model.train( input_fn=datasetImporter, steps=2000)


        raise NotImplementedError


'''

'''
class RetrievalSeq2SeqNNModel( modelz.ZModel ):

    '''
    setup  RNN layers 
    '''
    def init(self, name, removeStopWords=True): 
        super().init(name) 
        self.model = None
     
    '''
    '''
    def accuracy(self):
        raise NotImplementedError

    '''
    '''
    def predict(self, observation):
        raise NotImplementedError

    '''
    Input: 
        train_x : a list of sentences
    '''
    def train(self, train_x, train_y=None, test_x=None, test_y=None): 
        raise NotImplementedError
