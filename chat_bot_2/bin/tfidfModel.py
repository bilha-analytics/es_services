'''
author: bg
goal: TF-IDF based classifier
type: ZModel
refactor: 
'''

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk 

import pickle 

import zlogger

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
        super().init(name) 
        self.model = TfidfVectorizer(
            tokenizer = lemmatizeTokens,
            stop_words = "english" if removeStopWords else None,
            ngram_range = (1,3),             
        )

    '''
    '''
    def load(self, fpath=None):
        # 1. model definition 
        super().load(fpath) 
        # 2. training data 
        fpath = "{}.dat".format( self.model_fpath if fpath is None else fpath ) 
        try:
            with open( fpath, "rb") as fd:
                self.dataset = pickle.load(fd) 
                zlogger.log("{}.dataset.load".format(self.__class__), "Dataset loaded from file successfully")                
        except:
            zlogger.logError("{}.dataset.load".format(self.__class__), "Pickle to File - {}".format(fpath) ) 

    '''
    '''
    def dump(self, fpath=None): 
        # 1. model definition 
        super().dump(fpath)
        # 2. training data 
        fpath = "{}.dat".format( self.model_fpath if fpath is None else fpath ) 
        try:
            with open( fpath, "wb") as fd:
                pickle.dump( self.dataset, fd)  
                zlogger.log("{}.dataset.dump".format(self.__class__), "Dataset dumped to file successfully")                
        except:
            zlogger.logError("{}.dataset.dump".format(self.__class__), "Pickle to File - {}".format(fpath) ) 

    '''
    '''
    def accuracy(self):
        raise NotImplementedError

    '''
    TODO: alternative similarity measures Vs acurracy

    Input: a doc/sentence observation to find matching docs for
    Return: Doc with highest matching score or None if nothing found
    TODO: set a threshold for matching scores; don't just use max
    '''
    def predict(self, observation):                 
        sent_tokenz = self.dataset.copy()
        sent_tokenz.append( observation )       
        tfidf = self.model.fit_transform( sent_tokenz ) 

        valz = cosine_similarity( tfidf[-1], tfidf) 
        idx = valz.argsort()[0][-2] 
        flatz = valz.flatten()
        flatz.sort()

        resp = flatz[-2]

        if resp == 0:
            return None
        else:
            # return "{}\n\t{}".format(sent_tokenz[ idx ] , sent_tokenz[ idx+1])
            return "{}".format(sent_tokenz[ idx ] )

    '''
    Input: 
        train_x : a list of sentences
    '''
    def train(self, train_x, train_y=None, test_x=None, test_y=None): 
        self.dataset = train_x if isinstance(train_x, list ) else nltk.sent_tokenize( train_x )



if __name__ == "__main__":
    zlogger.log("tfidfModel.main", "Starting")

    src = "tfidfModel.main.test"
    named = "TFIDF_ChatBot"

    st = "The quick brown fox jumped over the lazy dogs. This is an account of a lost dog. His name was Jazzy and he had 7 bones. Hey there! Okay, bye." 

    for ist in [True, False]:
        wt = "Without" if ist else "With"
        zlogger.log(src, "\n\n{0} {1} Stop Words {0}".format("-"*7, wt ) ) 

        m = TfidfModel()
        m.init(named, removeStopWords=ist) 
        m.train( st ) 

        zlogger.log(src, "Data: {}\nModel: {}\n".format(st, m)  ) 

        xl = ["I see Jumping dogs", "You will be okay", "He's jumped that section", "There's a cat jumping over the fence"]
        for x in xl:
            zlogger.log(src,  "Observation: {}\n\tPrediction: {}\n".format(x, m.predict(x) ) ) 


        print( ">>>>> DUMPING ----", m.getClassName() )
        m.dump()

        m2 = TfidfModel()
        m2.load("{}.zmd".format(named) ) 
        
        x = "A jumping dog he is"
        zlogger.log(src,  "Observation: {}\n\tM2.Prediction: {}\n".format(x, m2.predict(x) ) )

    # zlogger.log(src,  ) 
    zlogger.log("tfidfModel.main", "Finished")
