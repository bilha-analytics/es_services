'''
author: bg
goal: 1. Train ncov19 @ TFIDF model. 2. Interact with it
type: service session 
refactor: class, 
'''

import zlogger
from botLogic import BotLogicFlow
from tfidfModel import TfidfModel 

import dataSet
import dataSource 

from termcolor import colored 


tfidif_model  = None
app_name = 'nCOV_bot'

'''
1. TRAIN 
Fetch text from web page
Setup TFIDF with that data
'''
def initiailizeBotEnv():
    global tfidif_model 
    src = "nCoV19_bot.initiailze"
    # 1. fetch data text 
    src = "https://en.wikipedia.org/wiki/Coronavirus_disease_2019"
    list_sentz = dataSource.readFrom( src, dataSource.zARTICLE ) 
    zlogger.log(src, "Loaded data text of size {}".format(len(list_sentz) ) ) 
    
    # 2. initialize and train model 
    tfidif_model = TfidfModel()
    tfidif_model.init( app_name ) 
    tfidif_model.train( list_sentz ) 
    zlogger.log(src, "Initiailized & Trained TF-IDF Model {}".format(tfidif_model) ) 

    # 3. save model
    tfidif_model.dump() 

'''
2. INTERACT 
RunBot Logic and UI
'''
def runBot(): 
    src = "nCoV19.runBot"    
    
    zlogger.log(src, "Starting")

    # 1. setup bot
    bot = BotLogicFlow()
    bot.initializeModel( bot.MODEL_TFIDF, "{}.zmd".format(app_name) )

    #2. run bot 
    while( 1 ):
        user_input = input( colored("Talk to me: ", "yellow") )
        prompt = colored( ">>>: ", "green") 

        response, rcode = bot.getResponse( user_input ) 

        print( "{} {}\n".format(prompt, "I don't understand. Try that again" if response is None else response )  ) 
        
        if ( rcode == -99) :
            break 
    
    zlogger.log(src, "Finished")



if __name__ == "__main__":
    initiailizeBotEnv()
    runBot()








