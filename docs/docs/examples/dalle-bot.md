---
sidebar_position: 5
---

# DALL-E bot
This bot makes an API call to OpenAI and processes the user input. It uses DALL-E.

**Do note that the `data_type` used is `IMAGE_URL` so that the images can be rendered on the chat UI.**
```py
from textbase import bot, Message
from textbase.models import DallE
from typing import List

# Load your OpenAI API key
DallE.api_key = ""

@bot()
def on_message(message_history: List[Message], state: dict = None):

    # Generate DallE response
    bot_response = DallE.generate(
        message_history=message_history, # Assuming history is the list of user messages
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
```