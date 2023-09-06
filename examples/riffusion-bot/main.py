from textbase import bot, Message
from textbase.models import RiffusionAI  # Import your RiffusionAI class
from typing import List

RiffusionAI.api_key = ""

SYSTEM_PROMPT = """You are chatting with an AI. There are no specific prefixes for responses, so you can ask or talk about anything you like.
The AI will respond in a natural, conversational manner. Feel free to start listeneing music of your lyrics.
"""

@bot()
def on_message(message_history: List[Message], state: dict = None):

    # Generate audio response based on user_message
    audio_url = RiffusionAI.generate(
        system_prompt=SYSTEM_PROMPT,
        message_history=message_history # Assuming history is the list of user messages
    ) 

    response = {
        "data": {
            "messages": [
                {
                    "data_type": "AUDIO",
                    "value": audio_url
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