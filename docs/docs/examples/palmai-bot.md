---
sidebar_position: 4
---

# Open AI bot

This bot makes an API call to Palm AI and processes the user input. It uses chat-bison-001

```py
from textbase import bot, Message
from textbase.models import Palm
from typing import List

# Load your PalmAI API key
Palm.api_key = ""

# Prompt for chat-bison-001
SYSTEM_PROMPT = """You are chatting with an AI. There are no specific prefixes for responses, so you can ask or talk about anything you like.
The AI will respond in a natural, conversational manner. Feel free to start the conversation with any question or topic, and let's have a
pleasant chat!
"""

@bot()
def on_message(message_history: List[Message], state: dict = None):

    # Generate Palm-model-chat-bison-001 response
    bot_response = Palm.generate(
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
```