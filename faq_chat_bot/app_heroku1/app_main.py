from flask import Flask, render_template, request 

import requests , json 

# import sys
# sys.path.append("../../../shared") 
import zlogger
import zdata_source
import zbot_logic
from zbot_logic import ZBotLogicFlow 

## 1. path to FAQ db
faq_path = [ ('1EuvcPe9WXSQTsmSqhq0LWJG4xz2ZRQ1FEdnQ_LQ-_Ks', 'FAQ responses!A1:G1000'), ('1EuvcPe9WXSQTsmSqhq0LWJG4xz2ZRQ1FEdnQ_LQ-_Ks', 'Classify_Phrases!A1:G1000')]
faq_typ = zdata_source.zGSHEET_FAQ
      
## 2. create bot
bot_app = ZBotLogicFlow()
bot_app.loadFaqDbz(faq_path, faq_typ)

## 3. load model 
bot_app.loadModel( zbot_logic.MODEL_COSINE_TFIDF, "cov_Cosine_Tfidf")
print( repr(bot_app.model.model) )

## 4. create flask app
app = Flask(__name__ )

MESSAGEZ = []

KE_DATA = None 
GLOBAL_DATA = None

def addMessage(src, msg):
    MESSAGEZ.append({
        'src': src ,
        'msg' : msg, 
    })

def getResponse(user_input):
    response, rcode = bot_app.getResponse( user_input ) 
    return "I don't understand. Try again differently" if response is None else response     


def getLatestSummaryStarts(country='Kenya'):
    global GLOBAL_DATA, KE_DATA
    api_url = "https://api.covid19api.com/summary"
    rqst = requests.get(api_url)
    print(rqst)
    rqst = json.loads( rqst.text )

    GLOBAL_DATA = rqst['Global']

    rqst = rqst['Countries']
    for item in rqst:
        if item['Country'] == country:
            KE_DATA = item

    print("KE: ", repr(KE_DATA ) ) 
    print("GLB: ", repr(GLOBAL_DATA ) ) 
    


@app.route("/", methods=['GET', 'POST'] ) 
def home():
    if request.method == 'POST':
        user_input = request.form.get('askBot')
        print( repr(user_input ) , len(user_input.strip() ) )  
        if user_input is not None and len( user_input.strip() ) > 0:
            answer = getResponse(user_input)  
            addMessage('in', user_input) 
            addMessage('out', answer) 
            zlogger.log('bot.chat', "User asked: {} ".format(user_input) ) 
            zlogger.log('bot.chat', "Bot answered: {} \n".format(answer) )  

    return render_template('layout_chat.html', 
                            scrollToAnchor='bottomz', 
                            msgs=MESSAGEZ, 
                            ke_data=KE_DATA,
                            glb_data=GLOBAL_DATA ) 


if __name__ == "__main__":
    
    getLatestSummaryStarts()

    app.run( debug=True) 