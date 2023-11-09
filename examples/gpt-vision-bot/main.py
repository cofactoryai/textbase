from typing import List
from textbase import bot, Message
from textbase.models import OpenAI

# Load your OpenAI API key
OpenAI.api_key = "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"

@bot()
def on_message(message_history: List[Message], state: dict = None):
    last_message = message_history[-1]['content'][-1]
    data_type = last_message['data_type']

    if data_type == "IMAGE_URL":
        bot_response = OpenAI.vision(
            message_history=message_history, # Assuming history is the list of user messages
            model="gpt-4-vision-preview",
        )
    elif data_type == "STRING":
        bot_response = OpenAI.vision(
            message_history=message_history,  # Assuming history is the list of user messages
            model="gpt-4-vision-preview",
        )

    return {
        "messages": [bot_response],
        "state": state
    }
