from textbase import bot, Message
from typing import List
from textbase.models import BardAI

@bot()
def on_message(message_history: List[Message], state: dict = None):

    bot_response = BardAI.generate(message_history=message_history)
  
    response = {
        "data": {
            "messages": [
                {
                    "data_type": "STRING",
                    "value": bot_response
                }
            ],
            "state": state
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