---
sidebar_position: 2
---

# Google PaLM AI bot

This bot makes an API call to PaLMAI and processes the user input. It uses PaLM Chat.

```py
import os
from textbase import bot, Message
from textbase.models import PalmAI
from typing import List

# Load your PALM API key
# PALMAI.api_key = ""
# or from environment variable:
PalmAI.api_key = os.getenv("PALM_API_KEY")

@bot()
def on_message(message_history: List[Message], state: dict = None):

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

```