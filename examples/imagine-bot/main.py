from textbase import bot, Message
from textbase.models import CreateImage
from typing import List

# Load your OpenAI API key
CreateImage.api_key = ""

# Prompt for GPT-3.5 Turbo
SYSTEM_PROMPT = """This is an image generation bot"""

@bot()
def on_message(message_history: List[Message], state: dict = None):
    if(len(message_history) == 0):
        return {
            "status_code": 400,
            "response": "Bad request"
        }

    bot_response = CreateImage.generate(
        message=message_history[len(message_history) - 1]
    )

    response = {
        "data": {
            "messages": [
                {
                    "data_type": "IMAGE_URL",
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