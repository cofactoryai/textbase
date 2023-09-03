from textbase import bot, Message
from textbase.models import DallE
from typing import List

# Load your OpenAI API key
DallE.api_key = ""

@bot()
def on_message(message_history: List[Message], state: dict = None):

    # Generate DallE response
    bot_response = DallE.generate(
        message_history=message_history, # Assuming history is the list of user messages
    )

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