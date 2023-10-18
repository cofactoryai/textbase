---
sidebar_position: 5
---

# DALL-E bot
This bot makes an API call to OpenAI and processes the user input. It uses DALL-E.

**You must import the `Image` datatype and wrap your bot_response with it so that the images can be rendered on the chat UI.**
```py
from typing import List
from textbase import bot, Message
from textbase.models import DallE
from textbase.datatypes import Image

# Load your OpenAI API key
DallE.api_key = ""

@bot()
def on_message(message_history: List[Message], state: dict = None):

    # Generate DallE response
    bot_response = DallE.generate(
        message_history=message_history, # Assuming history is the list of user messages
    )

    return {
        "messages": [Image(url=bot_response)],
        "state": state
    }
```