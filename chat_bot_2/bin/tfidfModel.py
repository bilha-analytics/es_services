from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import nltk

import pickle 
import traceback , sys 

import zlogger, logging

import modelz 
from dataSet import lemmatizeTokens

'''
Use TF-IDF to represent documents.
Use Similarity measures like cosine similarity to classify 

'''
class TfidfModel( modelz.ZModel ):

# TfidfVectorizer( 
#   tokenizer=fetch_data,   << use dataSet.lemmatizeTokens
#   stop_words="english",   << remove stopwords 
#   ngram_range=(1,3),      << generate 2 and 3 word phrass along with the single words 
#   analyzer='word',        << mutex with tokenizer
#   min_df=0                << 
# )


    '''
    setup the TFIDF tokenizer 
    '''
    def init(self, name, removeStopWords=True): 
        self.name = name 
        self.model_fpath = "{}.zmd".format( self.name) 
        self.tfidfVectorizer = TfidfVectorizer(
            tokenizer = lemmatizeTokens,
            stop_words = "english" if removeStopWords else None,
            ngram_range = (1,3),             
        )

    '''
    '''
    def load(self, fpath=None):
        fpath = self.model_fpath if None else fpath
        try:
            with open( fpath, "rb") as fd:
                pickle.load( self.tfidfVectorizer, fd)  
        except:
            zlogger.logError("{}.model.dump".format(self.__name__), "Pickle to File - {}".format(fpath) ) 

    '''
    '''
    def dump(self, fpath=None): 
        fpath = self.model_fpath if None else fpath
        try:
            with open( fpath, "wb") as fd:
                pickle.dump( self.tfidfVectorizer, fd)  
        except:
            zlogger.logError("{}.model.dump".format(self.__name__), "Pickle to File - {}".format(fpath) ) 

    '''
    '''
    def accuracy(self):
        raise NotImplementedError

    '''
    TODO: alternative similarity measures Vs acurracy

    Input: a doc/sentence observation to find matching docs for
    Return: Doc with highest matching score or None if nothing found
    TODO: set a threshold for matching scores; do just use max
    '''
    def predict(self, observation):                 
        sent_tokenz = self.dataset.copy()
        sent_tokenz.append( observation )       
        tfidf = self.tfidfVectorizer.fit_transform( sent_tokenz ) 
        
        valz = cosine_similarity( tfidf[-1], tfidf) 
        idx = valz.argsort()[0][-2] 
        flatz = valz.flatten()
        flatz.sort()

        resp = flatz[-2]

        if resp == 0:
            return None
        else:
            return "{}\n\t{}".format(sent_tokenz[ idx ] , sent_tokenz[ idx+1])

    '''
    '''
    def train(self, train_x, train_y=None, test_x=None, test_y=None): 
        self.dataset = train_x if isinstance(train_x, list ) else nltk.sent_tokenize( train_x )



if __name__ == "__main__":
    zlogger.log("tfidfModel.main", "Starting")

    src = "tfidfModel.main.test"

    st = "The quick brown fox jumped over the lazy dogs. This is an account of a lost dog. His name was Jazzy and he had 7 bones. Hey there! Okay, bye." 

    for ist in [True, False]:
        wt = "Without" if ist else "With"
        zlogger.log(src, "\n{0} {1} Stop Words {0}".format("-"*7, wt ) ) 

        m = TfidfModel()
        m.init("TFIDF_ChatBot", removeStopWords=ist) 
        m.train( st ) 

        zlogger.log(src, "Data: {}\nModel: {}\n".format(st, m)  ) 

        xl = ["I see Jumping dogs", "You will be okay", "He's jumped that section", "There's a cat jumping over the fence"]
        for x in xl:
            zlogger.log(src,  "Observation: {}\n\tPrediction: {}\n".format(x, m.predict(x) ) ) 


    # zlogger.log(src,  ) 
    zlogger.log("tfidfModel.main", "Finished")
