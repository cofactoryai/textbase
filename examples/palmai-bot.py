import os
from textbase import bot, Message
from textbase.models import OpenAI, PalmAI
from typing import List

# Load your PalmAI API key
PalmAI.api_key = ""
# or from environment variable
PalmAI.api_key = os.getenv("PALMAI_API_KEY")

# Prompt for GPT-3.5 Turbo
SYSTEM_PROMPT = """You are chatting with an AI. There are no specific prefixes for responses, so you can ask or talk about anything you like.
You will respond in a natural, conversational manner. Feel free to start the conversation with any question or topic, and let's have a pleasant chat!
"""

@bot()
def on_message(message_history: List[Message], state: dict = None):

    bot_response = PalmAI.generate(
        system_prompt=SYSTEM_PROMPT,
        message_history=message_history
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
