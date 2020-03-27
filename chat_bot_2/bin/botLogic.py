'''
author: bg
goal: Logic at chat and 
type: util, factory
refactor: class, pre-set responses, 
'''

from tfidfModel import TfidfModel
from dataSet import lemmatizeTokens

from termcolor import colored 
import random

import zlogger

'''

Expectations
  - Load ES model to be used. Can choose type 
  - Receive user input and fetch appropriate response. Has defaults 
'''

class BotLogicFlow():

    ## PRESET REPONSES FOR CERTAIN CATEGORIES 
    GREETINGZ_INPUT = ["hi", "hello", "greetings", "sasa", "mambo", 'hey', "niaje", "vipi", "salut", "what's up", "are you there"]
    GREETINGZ_RESPONSE = [ "hi", "hey", "hello", "how may i help you today", "what can i do for you", "nice to hear from you", "how are you"]

    EXIT_INPUT = ["bye", "later", "baadaye", "quit"]
    EXIT_RESPONSE = ["bye", 'later', 'talk again soon', 'baadaye', 'great chatting with you']

    THANKS_INPUT = ['thanks', 'sounds good', 'asante', 'shukurani', 'shukran']
    THANKS_RESPONSE = ["you're welcome", "glad to be of help", "anytime",  'happy to be of assistance']


    ## AVAILABLE LEARNING MODELS 
    MODEL_TFIDF = 1 # is default?? 

    AVAILABLE_MODELZ = {
        MODEL_TFIDF : TfidfModel, 
    }


    '''
    Assumes that model has already been trained 
    '''
    def initializeModel(self, mtype, mpath=None):  
        self.loadModel(mtype, mpath) 

    def loadModel(self, mtype, mpath):
        self.model_type = mtype
        mclass = self.AVAILABLE_MODELZ.get(mtype, TfidfModel) 
        self.model = mclass() 
        self.model.load(mpath) 

    def getResponse(self, user_input_text): 
        response = None
        rcode = 200

        key_words = lemmatizeTokens( user_input_text ) 
        
        was_que = True

        for word in key_words:
            if word in self.GREETINGZ_INPUT:
                response = random.choice( self.GREETINGZ_RESPONSE) 
                was_que = False
                break
            elif word in self.THANKS_INPUT:
                response = random.choice( self.THANKS_RESPONSE )
                was_que = False
                break
            elif word in self.EXIT_INPUT:
                response = random.choice( self.THANKS_RESPONSE )+". "+random.choice( self.EXIT_RESPONSE )
                rcode = -99 
                return response, rcode 

        if was_que:
            response = self.model.predict( user_input_text ) 

        return response, rcode 


    
if __name__ == "__main__":    
    zlogger.log("botLogic.main", "Starting")

    bot = BotLogicFlow()
    bot.initializeModel( BotLogicFlow.MODEL_TFIDF, "TFIDF_ChatBot.zmd") 

    while( 1 ):
        user_input = input( colored("Talk to me: ", "yellow") )
        prompt = colored( ">>>: ", "green") 

        response, rcode = bot.getResponse( user_input ) 

        print( "{} {}\n".format(prompt, "I don't understand. Try that again" if response is None else response )  ) 
        
        if ( rcode == -99) :
            break 
    
    zlogger.log("botLogic.main", "Finished")
    
