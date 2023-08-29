---
sidebar_position: 3
---

# Usage of decorator with example and response structure
This particular example uses OpenAI's API. You can use your own or you can even integrate some in the project itself. We are open for contributions!
```py
from textbase_framework import bot, Message
from textbase_framework.models import OpenAI

OpenAI.api_key = os.getenv("OPENAI_API_KEY")

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