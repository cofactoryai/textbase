from textbase import bot, Message
from textbase.models import OpenAI
from typing import List
import openai

# Load your OpenAI API key
OpenAI.api_key = "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"

# Prompt for GPT-3.5 Turbo
SYSTEM_PROMPT = """You are chatting with a movie recommendation system."""


@bot()
def on_message(message_history: List[Message], state: dict = None):

    # Generate GPT-3.5 Turbo response
    bot_response = OpenAI.generate(
        system_prompt=SYSTEM_PROMPT,
        message_history=message_history,  # Assuming history is the list of user messages
        model="gpt-3.5-turbo",
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
