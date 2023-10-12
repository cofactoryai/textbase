from typing import List
from textbase import bot, Message

@bot()
def on_message(message_history: List[Message], state: dict = None):

    # Mimic user's response
    bot_response = [message["value"] for message in message_history[-1]["content"]]

    # message_history[-1]["content"] structure is

    # [
    #     {
    #         "data_type": "STRING",
    #         "value": "<string value>"
    #     }
    # ]

    return {
        "messages": bot_response,
        "state": state
    }