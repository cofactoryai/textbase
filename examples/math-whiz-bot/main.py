from textbase import bot, Message
from typing import List
import re

@bot()
def on_message(message_history: List[Message], state: dict = None):

    user_message = message_history[-1]["content"][0]["value"]

    if user_message.lower().startswith("calculate:"):
        expression = user_message[len("calculate:"):].strip()
        try:
            result = eval(expression)
            bot_response = f"Result: {result}"
        except Exception as e:
            bot_response = f"Error: {str(e)}"
    else:
        bot_response = "I can help you with calculations. Please start your message with 'calculate:' followed by an expression."

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
        "errors": []
    }

    return {
        "status_code": 200,
        "response": response
    }
