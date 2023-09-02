import os
from textbase import bot, Message
from textbase.models import PalmAI
from typing import List

# Load your OpenAI API key
# OpenAI.api_key = ""
# or from environment variable:
PalmAI.api_key = os.getenv("PALM_API_KEY")

# Prompt for GPT-3.5 Turbo
SYSTEM_PROMPT = """You are chatting with an AI. There are no specific prefixes for responses, so you can ask or talk about anything you like.
You will respond in a natural, conversational manner. Feel free to start the conversation with any question or topic, and let's have a pleasant chat!
"""

@bot()
def on_message(message_history: List[Message], state: dict = None):

    # Generate GPT-3.5 Turbo response
    bot_response = PalmAI.generate(
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
