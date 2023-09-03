---
sidebar_position: 3
---

# Llama bot

This bot makes an API call to Meta's LLama 2 API and processes the user input. It uses Llama-2-7B model.

```py
from textbase import bot, Message
from textbase.models import Llama
from typing import List

# Load your Replicate API key
Llama.replicate_api_key = "r8_8xsgb2mpX8GB9Iz9BduNR3vwc0vs7Ei1zFi3u"

# Default Prompt for Llama7b. States how the AI Model is supposed to act like
SYSTEM_PROMPT = """\
You are a helpful assistant"""

@bot()
def on_message(message_history: List[Message], state: dict = None):

    # Generate Llama7b responses
    bot_response = Llama.generate(
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