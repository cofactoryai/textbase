---
sidebar_position: 1
---

# Mimicking bot

This bot just returns whatever the user has typed in.

```py
from textbase import bot, Message
from typing import List

@bot()
def on_message(message_history: List[Message], state: dict = None):

    # Mimic user's response
    bot_response = []
    bot_response = message_history[-1]["content"]

    response = {
        "data": bot_response,
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