from textbase import bot, Message
from typing import List

@bot()
def on_message(message_history: List[Message], state: dict = None):

    # Mimic user's response
    bot_response = message_history[-1]["content"]

    # message_history[-1]["content"] structure is 

    # [
    #     {
    #         "data_type": "STRING",
    #         "value": "<string value>"
    #     }
    # ]
    

    response = {
        "data": {
            "messages": bot_response,
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