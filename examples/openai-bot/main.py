import os
from textbase import bot, Message
from textbase.models import OpenAI
from typing import List
from prompt import PROMPT_TEXT
from dotenv import load_dotenv

load_dotenv()
# Load your OpenAI API key
OpenAI.api_key =os.getenv("OPEN_API_KEY")

# Prompt for GPT-3.5 Turbo
SYSTEM_PROMPT = PROMPT_TEXT

@bot()
def on_message(message_history: List[Message], state: dict = None):

    # Generate GPT-3.5 Turbo response
    bot_response = OpenAI.generate(
        system_prompt=SYSTEM_PROMPT,
        message_history=message_history, # Assuming history is the list of user messages
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