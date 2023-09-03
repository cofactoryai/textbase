from textbase import bot, Message
from typing import List
import pyttsx3




def speak(text):
    engine = pyttsx3.init('sapi5')  
    
    try:
        pass
        engine.say(text)    
        engine.startLoop(True)
    
    except:
        pass
        engine.stop()
    
    




@bot()
def on_message(message_history: List[Message], state: dict = None):

    # Mimic user's response
    bot_response = []
    bot_response = message_history[-1]["content"]
    mylist=[]+message_history[-1]["content"]
    response = {
        "data": {
            "messages": bot_response,
            "state": state,
            "speak": speak(mylist[0]["value"])
        },
        "errors": [
            {
                "message": ""
            }
        ]
    }

    return {
        "status_code": 200,
        "response": response
    }