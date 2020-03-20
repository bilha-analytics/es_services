from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import fetch_dataset


'''
    Find similarity between user input and corpus using TF-IDF and cosine similarity measure
    input = user_input_text and domain_corpus
    reurn = most suitable response
'''
_modelTfidVec = None

def presetCorpusTfidf():
    global _modelTfidVec
    _modelTfidVec = TfidfVectorizer( tokenizer=fetch_dataset.preProcessText, stop_words="english")
    
def tfidf_fetchQueResponse(input_text): 
    sent_tokenz = fetch_dataset._sentz.copy()
    sent_tokenz.append( input_text )       
    tfidf = _modelTfidVec.fit_transform( sent_tokenz ) 
    valz = cosine_similarity( tfidf[-1], tfidf) 
    idx = valz.argsort()[0][-2] 
    flatz = valz.flatten()
    flatz.sort()

    resp = flatz[-2]

    if resp == 0:
        return "I'm sorry, I don't understand. Try again"
    else:
        return "{} {} {}".format(sent_tokenz[ idx ] , sent_tokenz[ idx+1], sent_tokenz[ idx+2]  )


def initialize():    
    fetch_dataset.createCorpusSentenses()  
    presetCorpusTfidf( )

if __name__ == "__main__":
    initialize() 
    print("BOT: {}".format( tfidf_fetchQueResponse( "What is COVID-19?")    ) )
