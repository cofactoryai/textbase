---
sidebar_position: 1
---

# Mimicking bot

This bot just returns whatever the user has typed in.

```py
from textbase_framework import bot, Message
from textbase_framework.models import get_contents
from typing import List

@bot()
def on_message(message_history: List[Message], state: dict = None):

    # Mimic user's response
    bot_response = []
    bot_response = get_contents(message_history[-1], "STRING")

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