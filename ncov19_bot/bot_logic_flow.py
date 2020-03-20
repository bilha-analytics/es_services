import random 
import fetch_dataset
import retriever_model 


GREETINGZ_INPUT = ["hi", "hello", "greetings", "sasa", "mambo", 'hey', "niaje", "vipi", "salut", "what's up", "are you there"]
GREETINGZ_RESPONSE = [ "hi", "hey", "hello", "how may i help you today", "what can i do for you", "nice to hear from you", "how are you"]

EXIT_INPUT = ["bye"]
EXIT_RESPONSE = ["bye", "thank you", 'later', 'talk again soon', 'baadaye', 'great chatting with you']

THANKS_INPUT = ['thanks', 'sounds good', 'asante', 'shukurani', 'shukran']
THANKS_RESPONSE = ["you're welcome", "glad to be of help", "anytime", 'would you like anything else', 'happy to be of assistance']

_model = None


def greetings(input_text):
    for word in input_text.split():
        if word.lower() in GREETINGZ_INPUT:
            return random.choice( GREETINGZ_RESPONSE )


def thanks(input_text):
    for word in input_text.split():
        if word.lower() in THANKS_INPUT:
            return random.choice( THANKS_RESPONSE )


def byes(input_text):
    for word in input_text.split():
        if word.lower() in EXIT_INPUT:
            return random.choice( EXIT_RESPONSE )

def inputResponse(input_text):
    return retriever_model.tfidf_fetchQueResponse(input_text) 


def runBot():
    flag = True

    retriever_model.initialize() 

    while flag:
        user_input = input( "\033[94m Talk to me >>>: \033[0m") 

        response = "\033[92m \033[1m >>>: \033[0m"

        was_que = True
        for word in user_input.split():
            word = word.lower() 
            if word in GREETINGZ_INPUT:
                response += random.choice( GREETINGZ_RESPONSE) 
                was_que = False
                break
            elif word in THANKS_RESPONSE:
                response += random.choice( THANKS_RESPONSE )
                was_que = False
                break
            elif word in EXIT_INPUT:
                response += random.choice( THANKS_RESPONSE )+" "+random.choice( EXIT_RESPONSE ) 
                print( "{}\n".format(response )  )
                return(0) 

        if was_que:
                response += inputResponse( user_input )

        print( "{}\n".format(response )  )
        


if __name__ == "__main__":
    runBot( )