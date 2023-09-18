---
sidebar_position: 3
---
# Bot examples with response structures
## Bot example with response structure for text generation
This particular example uses OpenAI's API. You can use your own or you can even integrate some in the project itself. We are open for contributions!
```py
from textbase import bot, Message
from textbase.models import OpenAI

OpenAI.api_key = ""

# System prompt; this will set the tone of the bot for the rest of the conversation.

SYSTEM_PROMPT = """You are chatting with an AI. There are no specific prefixes for responses, so you can ask or talk about anything you like.
The AI will respond in a natural, conversational manner. Feel free to start the conversation with any question or topic, and let's have a
pleasant chat!
"""

@bot() #The decorator function
def on_message(message_history: List[Message], state: dict = None):

    # Your logic for the bot. A very basic request to OpenAI is provided below. You can choose to handle it however you want.
    bot_response = OpenAI.generate(
        model="gpt-3.5-turbo",
        system_prompt=SYSTEM_PROMPT,
        message_history=message_history
    )

    '''
    The response structure HAS to be in the format given below so that our backend framework has no issues communicating with the frontend.
    '''

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

## Bot example with response structure for image generation
This particular example uses DALL-E's API. You can use your own or you can even integrate some in the project itself. We are open for contributions!

**Make sure that you have given the `data_type` as `IMAGE_URL` whenever you have an image URL so that it can be properly rendered in the chat UI.**
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