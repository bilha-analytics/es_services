'''
author: bg
goal: 
type: 
refactor: class, encoders and selectors decouple
'''
import sys
sys.path.append("../../../shared") 
import zlogger 
import zdata_source


import string, re 

import nltk
from nltk.corpus import stopwords

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

import numpy as np 
import pandas as pd 

ZENC_ONEHOT = 1
ZENC_COUNT = 2
ZENC_TFIDF = 3
ZENC_EMBED = 4

ZLEVEL_CHAR = 1
ZLEVEL_WORD = 2
ZLEVEL_SUBWORDS = 3 #phonemes 
ZLEVEL_PHRASES = 4 #n-gram, POS, 
ZLEVEL_SENT = 5


'''
Preprocessing, encoding and filtering helpers 
TODO: word Vs char Vs sentense level
'''

'''
Convert text to lower + remove punctuations 
Input: a list of texts 
return: a list of tokens 
'''
def cleanup_case_and_puncts(*text): 
    tokenz = text
    punctuations = dict( (ord(p), None) for p in string.punctuation )
    # print(">>> {}".format( repr(tokenz) ) ) 
    tokenz = " ".join( [ t for t in tokenz ] ) 
    return np.array( nltk.word_tokenize( tokenz.lower().translate( punctuations) ) ) 

'''
Remove stop words 
Input: 
    text: a list of texts tokens 
    stop_wordz: default is nltk.english 
return: a list of tokens 
'''
def cleanup_stopwords(*text, stop_wordz=None):
    tokenz = text
    stopz = stopwords.words('english') if stop_wordz is None else stop_wordz 
    return np.array([w for w in tokenz if not w.lower() in stopz ] )

'''
Remove numerics 
Input: a list of texts tokens 
return: a list of tokens 
'''
def cleanup_numbers(*text, stop_wordz):
    tokenz = text
    return np.array([ w for w in tokenz if w.isalpha() ])

'''
Clean up text: 
Input: 
    text: a list of texts tokens , 
        :   what operations
return: a list of tokens 
'''
def cleanup_text(*text, remove_stopwordz=False, stop_wordz=None, remove_numberz=False):
    tokenz =  cleanup_case_and_puncts( *text ) 
    if remove_stopwordz:
        tokenz = cleanup_stopwords(tokenz, stop_wordz=stop_wordz) 
    if remove_numberz:
        tokenz = cleanup_numbers( tokenz ) 
    return np.array(tokenz )
   
'''
Use WordNetLemmatizer english dict

Input:  
Output:  
'''
def lemmatizeTokens(*text, remove_stopwordz=False, stop_wordz=None, remove_numberz=False):
    tokenz = cleanup_text( *text, 
        remove_stopwordz=remove_stopwordz, stop_wordz=stop_wordz, 
        remove_numberz=remove_numberz) 

    lemmatizer = nltk.stem.WordNetLemmatizer() 

    return sorted( [ lemmatizer.lemmatize( token )  for token in tokenz ] ) 


'''
TODO: review 
Input:  
Output:  
'''
def cleanup_and_lemmatize(*text, remove_stopwordz=False, stop_wordz=None, remove_numberz=False, lemmatized=True):
    return lemmatizeTokens( 
                *text, 
                remove_stopwordz=remove_stopwordz, stop_wordz=stop_wordz, 
                remove_numberz=remove_numberz
            ) if lemmatized else cleanup_text( 
                *text, 
                remove_stopwordz=remove_stopwordz, stop_wordz=stop_wordz, 
                remove_numberz=remove_numberz)

'''
word tokens without punct, lemmatize, get unique set

Input:  
Output:  
'''
def getVocabList(*text, remove_stopwordz=False, stop_wordz=None, remove_numberz=False, lemmatized=False):
    vocab = cleanup_and_lemmatize( *text, 
        remove_stopwordz=remove_stopwordz, stop_wordz=stop_wordz, 
        remove_numberz=remove_numberz, lemmatized=lemmatized) 
    return sorted( set( vocab ) ) 

'''
Operates
Input:  
Output: (vocab_vec, matrix) Vocab used and matrix per sentence encoded. 
'''
def onehotEncode(*text, remove_stopwordz=False, stop_wordz=None, remove_numberz=False, lemmatized=False):
    vocab = getVocabList( *text, 
        remove_stopwordz=remove_stopwordz, stop_wordz=stop_wordz, 
        remove_numberz=remove_numberz, lemmatized=lemmatized ) 

    vect = onehotVectorizer(vocab, *text)

    return vocab, vect

def onehotVectorizer(vocab, *text):
    vect = []
    for ln in text:
        tmp = np.zeros( len(vocab) ) 
        for i, v in enumerate(vocab):
            if v in ln.lower() :
                tmp[i] = 1
        vect.append( tmp )
    return np.array( vect )

'''
Operates
Input:  
Output: (count_vectorizer, res_matrix) Vectorizer used and matrix per sentence encoded. 
'''
def countEncode(*text, ngram_range=(1,1), **kwargz ):
    tokenz = cleanup_and_lemmatize( *text, 
            remove_stopwordz=kwargz['remove_stopwordz'], stop_wordz=kwargz['stop_wordz'], 
            remove_numberz=kwargz['remove_numberz'], lemmatized=kwargz['lemmatized'] )
    
    cv = CountVectorizer( stop_words=kwargz['stop_wordz'], ngram_range=ngram_range ) 
    res_matrix = cv.fit_transform( tokenz ) #.toarray().atype('float32')

    return cv, res_matrix 


'''
Operates
Input:  
Output: (count_vectorizer, res_matrix) Vectorizer used and matrix per sentence encoded. 
'''
def tfidfEncode(*text, 
        remove_stopwordz=False, stop_wordz=None, remove_numberz=False, lemmatized=False, 
        ngram_range=(1,1)
        ):

    tokenz = cleanup_and_lemmatize( *text, 
            remove_stopwordz=remove_stopwordz, stop_wordz=stop_wordz, 
            remove_numberz=remove_numberz, lemmatized=lemmatized )
    
    cv = TfidfVectorizer( stop_words=stop_wordz, ngram_range=ngram_range ) 
    res_matrix = cv.fit_transform( tokenz ) #.toarray().atype('float32')

    return cv, res_matrix 


'''
Operates
Input:  
Output: (count_vectorizer, res_matrix) Vectorizer used and matrix per sentence encoded. 
'''
def embeddingEncode(*text, 
    remove_stopwordz=False, stop_wordz=None, remove_numberz=False, lemmatized=False, 
    ngram_range=(1,1)
    ):
    raise NotImplementedError 


'''
TODO:
'''
def doTrainEncode(enc_type, *text, **argz):
    params = ['remove_stopwordz', 'stop_wordz', 'remove_numberz','lemmatized']
    for p in params:
        if not p in argz.keys():
            argz[p] = None 

    encoder = dict_encoders.get(enc_type, ZENC_TFIDF) 
    return encoder( *text, **argz)  

'''
TODO: include preprocessing
'''
def doPredictEncode(enc_type, context, *text):
    result = None 

    if enc_type == ZENC_ONEHOT:
        result = onehotVectorizer(context, *text)

    elif enc_type == ZENC_COUNT or enc_type == ZENC_TFIDF:
        result = context.transform( text )        
    else:
        pass 

    return result


###########################################################
'''
'''

dict_encoders = {
    ZENC_ONEHOT : onehotEncode,
    ZENC_COUNT : countEncode, 
    ZENC_TFIDF : tfidfEncode,
    ZENC_EMBED : embeddingEncode
} # default = tfidf 

dict_selectors = {

}



'''
TODO: abstract class, iterable, own and encap a data
'''
class ZDataset():
    ## TODO: overloaded constructor 
    ## TODO: expand multiple data in one return e.g. (train, test) or (faq_db, train)
    def initFromSeq(self, data):
        self.data = data 
    def initFromResource(self, data_path, data_type): 
        self.load( data_path, data_type)

    def load(self, data_path, data_type):
        self.data_path = data_path
        self.data_type = data_type 
        self.data = zdata_source.readFrom(data_path, data_type) 

    def dumpSave(self, data_path=None, data_type=None):
        dpath = self.data_path if data_path is None else data_path 
        dtype = self.data_type if data_type is None else data_type
        zdata_source.writeTo(self.data, dpath, dtype=dtype) 

    '''
    Things done
        - to lower case 
        - remove punctuations 
        - remove stop words 
        - remove escape characters 
        - remove numbers 
        - lemmatize 
    '''
    def preprocess(self, remove_stopwordz=False, stop_wordz=None, remove_numberz=False, lemmatized=True, unique=True): 
        self.clean_data = cleanup_and_lemmatize(*self.data, 
            remove_stopwordz=remove_stopwordz, stop_wordz=stop_wordz, 
            remove_numberz=remove_numberz, lemmatized=lemmatized) 
        if unique:
            self.clean_data = sorted( set(self.clean_data ) ) 

    '''
    TODO: expand options and train Vs test/predict
    '''
    def encodeTrain(self,  enc_type=None):       
        self.context, self.encoded_matrix = doTrainEncode( enc_type, *self.clean_data  ) 
        self.enc_type = enc_type 
        return self.context, self.encoded_matrix 

    def encodePredict(self, *text):
        return doPredictEncode( self.enc_type, self.context,  *text) 
        


'''
'''
class ZGsheetFaqDataSet( ZDataset ):     
    def load(self, data_path, data_type):
        self.data_path = data_path
        self.data_type = data_type 
        self.faq_db, self.data = zdata_source.readFrom(data_path, data_type)  

    def category_to_index(self):
        pass    


###########################################################

if __name__ == "__main__":
    src = "dataset.main"
    zlogger.log(src, ">>>>> STARTING\n")
    
    st = "The quick brown fox jumped over the lazy dogs. This is an account of a lost dog. His name was Jazzy and he had 7 bones. Hey there! Okay, bye." 
    # st = nltk.sent_tokenize( st )

    ds = ["The quick brown fox", "He had 7 bones"] 

    ps = "The brown bones" # predict text 
    
    tokz = lemmatizeTokens(st)
    print( "Tokens len: {}\n{}\n".format( len(tokz), tokz) )
    

    dset = ZDataset()
    dset.initFromSeq( ds ) 
    dset.preprocess()     
    print( "Tokens len: {}\n{}\n".format( len(dset.clean_data), dset.clean_data ) ) 

    vocab, matrix = dset.encodeTrain(enc_type=ZENC_ONEHOT)
    zlogger.log(src+".OnehotEncode", "Vocab = {} \nMatrix = {}".format(len(vocab), matrix.shape) )
    print( "Context: {}\n Matrix: {}\n".format(vocab, matrix))
    res = dset.encodePredict(ps)
    zlogger.log(src+".OnehotEncodePredict", "Input = {} Encoding = {}".format(ps, res) )

    vocab, matrix = dset.encodeTrain(enc_type=ZENC_COUNT)
    zlogger.log(src+".CountEncode", "Vocab = {} \nMatrix = {}".format(vocab, matrix.shape) )
    print( "Context: {}\n Matrix: {}\n".format(vocab, matrix))
    res = dset.encodePredict(ps)
    zlogger.log(src+".CountEncodePredict", "Input = {} Encoding = {}".format(ps, res) )


    vocab, matrix = dset.encodeTrain(enc_type=ZENC_TFIDF)
    zlogger.log(src+".TfidfEncode", "Vocab = {} \nMatrix = {}".format(vocab, matrix.shape) )
    print( "Context: {}\n Matrix: {}\n".format(vocab, matrix))
    res = dset.encodePredict(ps)
    zlogger.log(src+".TfidfEncodePredict", "Input = {} Encoding = {}".format(ps, res) )

    zlogger.log(src, "=== From GSheet ===")
    faq_path = [ ('1EuvcPe9WXSQTsmSqhq0LWJG4xz2ZRQ1FEdnQ_LQ-_Ks', 'FAQ responses!A1:G1000'), ('1EuvcPe9WXSQTsmSqhq0LWJG4xz2ZRQ1FEdnQ_LQ-_Ks', 'Classify_Phrases!A1:G1000')]
    faq_typ = zdata_source.zGSHEET_FAQ


    dset = ZGsheetFaqDataSet()
    dset.initFromResource(faq_path, faq_typ)  
    dset.preprocess()     
    dlen =  len(dset.clean_data) 
    print( "Tokens len: {}\n{}\n".format(dlen, dset.clean_data[: min(dlen, 10) - 1 ] ) ) 

    vocab, matrix = dset.encodeTrain(enc_type=ZENC_TFIDF)
    zlogger.log(src+".TfidfEncode", "Vocab = {} \nMatrix = {}".format(vocab, matrix.shape) )
    print( "Context: {}\n Matrix: {}\n".format(vocab, matrix))
    res = dset.encodePredict(ps)
    zlogger.log(src+".TfidfEncodePredict", "Input = {} Encoding = {}".format(ps, res) )


    zlogger.log(src, "FINISHED <<<<<")
