'''
author: bg
goal: NN based Multi-class text classifiers. Retrieval supervised classifier, Retrieval Seq2Seq, Generative 
type: ZModel
refactor: 
'''

import tensorflow as tf
from tensorflow import keras 
import numpy as np 

import pickle 

import zlogger

import modelz 
import dataSource 
from dataSet import lemmatizeTokens


'''

'''
class RetrievalSupervisedNNModel( modelz.ZModel ):

    '''
    setup  RNN layers 
    Input:
        super @ name, removeStopwords
        faq_gsheet = Path to GSheet with faq_responses_db, faq_classify_phrases_db =  [(sheetID, sheetname_and_range), (sheetID, sheetname_and_range)]
    TODO: refactor @ setup Vs train call and internal Vs user axn 
    '''
    def init(self, name, removeStopWords=True, faq_gsheet=None, hash_featurez=False):  
        super().init(name) 
        src = 'RSNNModel.init'

        # these are dict( class_cat : response | question)
        self.faq_responses_db, self.faq_classify_phrases_db = dataSource.doGSheet_FAQ(faq_gsheet, dataSource.zGSHEET_FAQ) 
        # self.num_classes = len( self.faq_responses_db.keys() ) 

        self.class_categoriez = {} # force labelz into numerics TODO: refine reuse @priors
        for i, v in enumerate( self.faq_responses_db.keys() ) :
            self.class_categoriez[v] = i
        self.class_categoriez["I don't know yet. Will learn more"] = len(self.class_categoriez) 
        
        self.num_classes = len( self.class_categoriez )

        zlogger.log(src, self.showParams() )
        
        ## feature mappers
        feature_col_mapper = [
            tf.feature_column.embedding_column(
                categorical_column = tf.feature_column.categorical_column_with_hash_bucket(key='user_que', hash_bucket_size=100 ) if hash_featurez 
                    else tf.feature_column.categorical_column_with_identity('user_que'), 
                dimension = int(self.num_classes ** 0.25) 
            ) 
        ]


        self.model = tf.estimator.DNNClassifier(
            feature_columns = feature_col_mapper,
            hidden_units = [256, 128], # hyper params?? TODO: ref and param
            model_dir = self.getModelFPath(),
            n_classes = self.num_classes,
            # label_vocabulary = list( self.class_categoriez.keys() ) # if defined here then labelz can be string in map_input_fn below 
            
        )

    ## map data to tf.Estimator format TODO: place well 
    def map_input_train_data(self):
        featurez = {'user_que' : np.array( list(self.faq_classify_phrases_db.keys() ) ) }
        labelz = np.array( [self.class_categoriez.get(k, self.num_classes-1 ) for k in self.faq_classify_phrases_db.values() ] ) 
        # labelz = np.array( list(self.faq_classify_phrases_db.values() )  ) 
        return featurez, labelz 

    
    '''
    '''
    def accuracy(self):
        raise NotImplementedError

    '''
    '''
    def predict(self, observation):
        src = 'RSNNModel.predict'

        def map_input_predict_data():
            return { 'user_que': np.array([observation]) }  

        def fetchReponse(pred):
            pclass = self.class_categoriez.get(pred)
            return self.faq_responses_db.get( pclass, "I don't seem to know about that yet. I'll find out more")
            
        pred = self.model.predict( input_fn = map_input_predict_data ) 
        # pred = np.array( pred.get('predictions') ).argmax() 
        zlogger.log( src, " predicted value = {} e.g. {}".format( pred, pred ) ) 

        return fetchReponse( pred ) 

    
    '''
    Input: 
        train_x : pandas db Vs Gsheet workbook <<< list of rows e.g. at GSheet workbook @ classify phrases
    '''
    def train(self, train_x=None, train_y=None, test_x=None, test_y=None, epochs=25000): 
        self.model.train(input_fn=self.map_input_train_data , steps = epochs) 
        zlogger.log('RSNNModel.train', "FINISHED: {} epochs".format(epochs) ) 

    def showParams(self):
        return "Loaded {} responses, {} phrases and so {} classes".format(len(self.faq_responses_db), len(self.faq_classify_phrases_db), self.num_classes)

    def __str__(self):
        return "{}\n\t{}\n\t".format( super.__str__, self.showParams(), self.model )

'''

'''
class RSNNModelKeras( modelz.ZModel ):

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


if __name__ == "__main__":
    src = 'rnnModel.main'
    dpath = [ ('1EuvcPe9WXSQTsmSqhq0LWJG4xz2ZRQ1FEdnQ_LQ-_Ks', 'FAQ responses!A1:G1000'), ('1EuvcPe9WXSQTsmSqhq0LWJG4xz2ZRQ1FEdnQ_LQ-_Ks', 'Classify_Phrases!A1:G1000')]
    
    zlogger.log(src, 'STARTING')

    rnn = RetrievalSupervisedNNModel()
    rnn.init('DNNClassifier', faq_gsheet= dpath, hash_featurez=True ) 
    zlogger.log(src, "Model is:\n{}".format( rnn ) )

    #train
    rnn.train()
    zlogger.log(src, 'Done Training. Moving on to predict using trained model')

    #predict
    sentz = [ "Is my cat sick", "Is my cat sick with the virus", "Can an insect infect me", "What is corana", "What is corana virus", "What is covid-19"]

    for s in sentz:
        r = rnn.predict( s  ) 
        zlogger.log("{}.predict".format(src), "\n{} ==> {} ".format( s, r ) )

    zlogger.log(src, 'FINISHED')
