from typing import List
from textbase import bot, Message
from textbase.models import OpenAI

# Load your OpenAI API key
OpenAI.api_key = ""

# Prompt for GPT-3.5 Turbo
SYSTEM_PROMPT = """You are chatting with an AI. There are no specific prefixes for responses, so you can ask or talk about anything you like.
The AI will respond in a natural, conversational manner. Feel free to start the conversation with any question or topic, and let's have a
pleasant chat!
"""

@bot()
def on_message(message_history: List[Message], state: dict = None):
    last_message = message_history[-1]['content'][-1]
    data_type = last_message['data_type']

    if data_type == "IMAGE_URL":
        image_url = last_message['value']
        bot_response = OpenAI.vision(
            message_history=message_history, # Assuming history is the list of user messages
            model="gpt-4-vision-preview",
            image_url=image_url
        )
    elif data_type == "STRING":
        text = last_message['value']
        bot_response = OpenAI.vision(
            message_history=message_history,  # Assuming history is the list of user messages
            model="gpt-4-vision-preview",
            text=text
        )

    return {
        "messages": [bot_response],
        "state": state
    }
