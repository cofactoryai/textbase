---
sidebar_position: 3
---

# HuggingFace bot

This bot makes an API call to OpenAI and processes the user input. It uses Microsoft's [DialoGPT-large](https://huggingface.co/microsoft/DialoGPT-large) model.

```py
import os
from textbase_framework import bot, Message
from textbase_framework.models import HuggingFace
from typing import List

# Load your OpenAI API key
# HuggingFace.api_key = ""
# or from environment variable:
HuggingFace.api_key = os.getenv("HUGGINGFACE_API_KEY")

# Prompt for GPT-3.5 Turbo
SYSTEM_PROMPT = """You are chatting with an AI. There are no specific prefixes for responses, so you can ask or talk about anything you like.
The AI will respond in a natural, conversational manner. Feel free to start the conversation with any question or topic, and let's have a
pleasant chat!
"""

@bot()
def on_message(message_history: List[Message], state: dict = None):

    # Generate HuggingFace response. Uses the DialoGPT-large model from Microsoft by default.
    bot_response = HuggingFace.generate(
        system_prompt=SYSTEM_PROMPT,
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