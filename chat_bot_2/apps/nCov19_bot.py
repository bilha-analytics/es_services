'''
author: bg
goal: 1. Train ncov19 @ TFIDF model. 2. Interact with it
type: service session 
refactor: class, 
'''
import sys
sys.path.append("../bin")

import zlogger
from botLogic import BotLogicFlow
from tfidfModel import TfidfModel 

import dataSet
import dataSource 

from termcolor import colored 


tfidif_model  = None
app_name = 'nCOV_bot'
# faq_path = "https://www.health.nsw.gov.au/Infectious/alerts/Pages/coronavirus-faqs.aspx" #"https://www.who.int/news-room/q-a-detail/q-a-coronaviruses"
# faq_typ = dataSource.zARTICLE 

faq_gsheet_path = ('1EuvcPe9WXSQTsmSqhq0LWJG4xz2ZRQ1FEdnQ_LQ-_Ks', 'FAQ responses!A1:G1000')
faq_gsheet_typ = dataSource.zGSHEET
faq_path = "FAQ.txt"
faq_typ = dataSource.zFILE


'''
1. TRAIN 
Fetch text from web page
Setup TFIDF with that data
'''
def initiailizeBotEnv(src_path, src_type=dataSource.zFILE ):
    global tfidif_model 
    src = "nCoV19_bot.initiailze"

    # 1. fetch data text 
    list_sentz = dataSource.readFrom( src_path, src_type)   
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


## helper at fetch paragraphs in FAQ Gsheet
def unpack_FaqGsheet():     
    gsheet = dataSource.readFrom( faq_gsheet_path, dtype=faq_gsheet_typ)[1: ] ## ignore header row

    print( gsheet[0:2] )

    # responses = gsheet[,3]## unpack responses only 
    responses = []
    for row in gsheet:
        responses.append( row[2]) 

    dataSource.writeTo(responses, dpath=faq_path)  





if __name__ == "__main__":
    # initiailizeBotEnv("https://en.wikipedia.org/wiki/Coronavirus_disease_2019",      dataSource.zARTICLE)

    unpack_FaqGsheet()

    # initiailizeBotEnv(faq_path, faq_typ)
    # runBot()








