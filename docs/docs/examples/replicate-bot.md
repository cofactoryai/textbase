---
sidebar_position: 3
---

# Replicate bot

This bot makes an API call to Replicate and processes the user input. It uses Facebook's [Llama-2-13b-chat](https://replicate.com/a16z-infra/llama-2-13b-chat) model.

```py
from textbase import bot, Message
from textbase.models import Replicate
from typing import List

# Load your Replicate API key
Replicate.api_key = "r8_MrTf8Dfd0UzLeCpLQjOIg4oW5yu9uQK0XohS1"

# Prompt for Llama 2
SYSTEM_PROMPT = """You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe.
Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content.
Please ensure that your responses are socially unbiased and positive in nature. If a question does not make any sense,
or is not factually coherent, explain why instead of answering something not correct.
If you don't know the answer to a question, please don't share false information.
"""

@bot()
def on_message(message_history: List[Message], state: dict = None):

    # Generate Llama 2 response
    bot_response = Replicate.generate(
        system_prompt=SYSTEM_PROMPT,
        message_history=message_history, # Assuming history is the list of user messages
        model="a16z-infra/llama-2-13b-chat:9dff94b1bed5af738655d4a7cbcdcde2bd503aa85c94334fe1f42af7f3dd5ee3",
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