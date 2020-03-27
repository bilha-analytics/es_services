from flask import Flask, render_template, request
# from chatterbot import ChatBot 
# from chatterbot.trainers import ChatterBotCorpusTrainer
# from chatterbot.trainers import ListTrainer


app = Flask(__name__ )

# bot = None 

# def setupBot(name="Testerizer"):
#     global bot
#     bot = ChatBot( name )
#     bot.set_trainer( ListTrainer )
#     bot.set_trainer( ChatterBotCorpusTrainer ) 
#     bot.train('chatterbot.corpus.english') 


@app.route('/')
def home():
    return render_template('home.html') 

@app.route('/get') 
def get_bot_response(): 
    input_text = request.args.get('msg')
    return "Thanks. You said: {}".format( input_text ) 


if __name__ == "__main__":
    app.run()