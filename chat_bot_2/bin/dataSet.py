'''
author: bg
goal: preprocess & generate appropriate list of word or sentence tokens. Does not vectorize but may have helper functions
type: util, factory
refactor: class
'''

import dataSource

import zlogger, logging
import sys, traceback

import nltk
import string 
import numpy as np 

from nltk.corpus import stopwords

''' 
TODO: all return a dataset so can chain requests. Collection of decorators
'''

'''
Turn prose to a list of sentences. 
Set all to lower case?? << TODO: what about named entity issues; don't lower case for now and rethink

Input: Free form text to be tokenized to a list of sentences. 
Output: list of sentences
'''
def initiateDataset(text_content):
    return nltk.sent_tokenize( text_content ) 

'''
Use nltk english puctuations dict. 
Replace all punctions with None

Input: dataset to be operated on. Must be a list (or array or vector)
Output: lower case word tokens after operation 
'''
def wordTokenizeWithoutPunctuations(dataset):
    punctuations = dict( (ord(p), None) for p in string.punctuation )
    text = dataset if isinstance(dataset, str) else " ".join(dataset)
    return nltk.word_tokenize( text.lower().translate( punctuations) ) 

'''
TODO: when and what to keep

Input: tokenz list to be operated on
Output: token list after operation 
'''
def removeNonWords_Tokens(tokenz):
    return [ w for w in tokenz if w.isalpha() ]
'''
Use nltk stopwords listing for english 

Input: tokens list to be operated on
Output: tokens list after operation 
'''
def removeStopWords_Tokens(tokenz):
    stopz = stopwords.words('english')
    return [w for w in tokenz if not w.lower() in stopz ] 

'''
Use WordNetLemmatizer english dict

Input: dataset to be operated on
Output: dataset after operation 
'''
def lemmatizeTokens(tokenz ):
    lemertizer = nltk.stem.WordNetLemmatizer() 
    tokenz =  wordTokenizeWithoutPunctuations( tokenz )  
    return sorted( [ lemertizer.lemmatize( token )  for token in tokenz ] ) 

'''
word tokens without punct, lemmatize, get unique set

Input: dataset to be operated on
Output: dataset after operation 
'''
def getVocabList(dataset):
    tokenz = wordTokenizeWithoutPunctuations( dataset )
    tokenz = removeNonWords_Tokens( removeStopWords_Tokens(tokenz ) ) 
    return sorted( set( lemmatizeTokens( tokenz ) ) ) 

'''
Operates per sentence

Input: dataset to be operated on
Output: (vocab, matrix) Vocab used and matrix per sentence encoded. 
'''
def oneHotEncode_LemmaBagOfWords(dataset): 
    vocab = getVocabList( dataset ) 
    dataset = dataset if isinstance(dataset, list) else nltk.sent_tokenize( dataset ) 

    vect = []
    for ln in dataset:
        tmp = np.zeros( len(vocab) ) 
        for i, v in enumerate(vocab):
            if v in ln.lower() :
                tmp[i] = 1
        vect.append( tmp )

    return vocab, np.array(vect ) 
'''
Input: dataset to be operated on
Output: dataset after operation 
'''

if __name__ == "__main__":
    st = "The quick brown fox jumped over the lazy dogs. This is an account of a lost dog. His name was Jazzy and he had 7 bones. Hey there! Okay, bye." 

    zlogger.log("dataSet.main", "Starting")

    src = "dataSet.main.example"

    df = initiateDataset( st )
    zlogger.log(src, "Dataset of {} lines".format( len(df) ) )
    print( df , "\n")

    tokenz = wordTokenizeWithoutPunctuations(df) 
    vocab = getVocabList( df ) 
    zlogger.log(src, "There are {} words and {} vocab".format(len(tokenz), len(vocab) ) )
    print( "{}\n{}\n".format(tokenz, vocab) )

    vocab, matrix = oneHotEncode_LemmaBagOfWords(st)
    zlogger.log(src, "Vocab = {} Matrix = {}".format(len(vocab), matrix.shape) )
    print( "{}\n{}\n".format(vocab, matrix))


    zlogger.log("dataSet.main", "Finished")