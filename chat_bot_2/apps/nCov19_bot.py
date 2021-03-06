'''
author: bg
goal: 1. Train ncov19 @ TFIDF model. 2. Interact with it
type: service session 
refactor: class,  use of gsheet db as own entity 
'''
import sys
sys.path.append("../bin")

import zlogger
import botLogic
from botLogic import BotLogicFlow
from tfidfModel import TfidfModel 

import dataSet
import dataSource 
import modelz 

from termcolor import colored 


model  = None
app_name = 'nCOV_bot'
# faq_path = "https://www.health.nsw.gov.au/Infectious/alerts/Pages/coronavirus-faqs.aspx" #"https://www.who.int/news-room/q-a-detail/q-a-coronaviruses"
# faq_typ = dataSource.zARTICLE 

faq_path = [ ('1EuvcPe9WXSQTsmSqhq0LWJG4xz2ZRQ1FEdnQ_LQ-_Ks', 'FAQ responses!A1:G1000'), ('1EuvcPe9WXSQTsmSqhq0LWJG4xz2ZRQ1FEdnQ_LQ-_Ks', 'Classify_Phrases!A1:G1000')]
faq_typ = dataSource.zGSHEET_FAQ

gsheet_faq_db = None 
gsheet_faq_training_set_db = None 

# model types

'''
1. TRAIN 
Fetch text from web page
Setup TFIDF with that data
'''
def initiailizeBotEnv(src_path, src_type=dataSource.zFILE, model_type=botLogic.MODEL_TFIDF, nostopwords=True): 
    global model , gsheet_faq_db, gsheet_faq_training_set_db 

    src = "nCoV19_bot.initiailze"

    # 1. fetch data text 
    list_sentz = None 
    if src_type == dataSource.zGSHEET_FAQ:
        gsheet_faq_db, gsheet_faq_training_set_db = dataSource.doGSheet_FAQ(src_path, src_type)
        list_sentz = list( gsheet_faq_training_set_db.keys()  ) 
    else:
        list_sentz = dataSource.readFrom( src_path, src_type)   
        
    zlogger.log(src, "Loaded data text of size {}".format(len(list_sentz) ) ) 
    
    # 2. initialize and train model 
    model = botLogic.AVAILABLE_MODELZ.get(model_type, TfidfModel)
    model = model() 
    model.init( app_name, removeStopWords=nostopwords ) 
    model.train( list_sentz ) 
    zlogger.log(src, "Initiailized & Trained TF-IDF Model {}".format(model) ) 

    # 3. save model
    model.dump() 

'''
2. INTERACT 
RunBot Logic and UI
'''
def runBot(isGsheetDB=False, model_type=botLogic.MODEL_TFIDF,): 
    src = "nCoV19.runBot"    
    
    zlogger.log(src, "Starting")

    # 1. setup bot
    bot = BotLogicFlow()
    bot.initializeModel( model_type,  "{}.zmd".format(app_name) )

    #2. run bot 
    while( 1 ):
        user_input = input( colored("Talk to me: ", "yellow") )
        prompt = colored( ">>>: ", "green") 

        response, rcode = bot.getResponse( user_input ) 

        if isGsheetDB and response and rcode == BotLogicFlow.RCODE_LEARNT_RESPONSE:
            idx = gsheet_faq_training_set_db.get( response, None) # fetch class name  
            
            zlogger.log( src, idx ) 
            
            response = gsheet_faq_db.get(idx, "I don't know that yet. I'll find out more") 

        print( "{} {}\n".format(prompt, "I don't understand. Try that again" if response is None else response )  ) 
        
        if ( rcode == BotLogicFlow.RCODE_EXIT_RESPONSE) :
            break 
    
    zlogger.log(src, "Finished")


## helper at fetch paragraphs in FAQ Gsheet
def unpack_FaqGsheet(dpath):     
    global gsheet_faq_db, gsheet_faq_training_set_db

    ## 1. unpack responses set @ retrieval 
    gsheet_faq_db = {} 
    tmp = dataSource.readFrom( dpath, dtype=dataSource.zGSHEET )[1: ] ## ignore header row
    for row in tmp:
        if len(row) > 2:
            gsheet_faq_db[ row[1] ] = row[2]

    ## 2. unpack training set        
    gsheet_faq_training_set_db = {}
    tmp = dataSource.readFrom( training_question_set, dtype=dataSource.zGSHEET )[1: ]
    for row in tmp:
        if len(row) > 1:
            gsheet_faq_training_set_db[ row[0] ] = row[1] 




if __name__ == "__main__":
    # initiailizeBotEnv("https://en.wikipedia.org/wiki/Coronavirus_disease_2019",      dataSource.zARTICLE)
    nostopwords = False
    initiailizeBotEnv(faq_path, faq_typ, nostopwords=nostopwords)
    runBot( faq_typ == dataSource.zGSHEET_FAQ ) 








