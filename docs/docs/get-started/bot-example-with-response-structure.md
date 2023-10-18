---
sidebar_position: 4
---
# Bot examples with response structures
## Bot example for text generation
This particular example uses OpenAI's API. You can use your own or you can even integrate some in the project itself. We are open for contributions!
```py
from typing import List
from textbase import bot, Message
from textbase.models import OpenAI

# Load your OpenAI API key
OpenAI.api_key = ""

# Prompt for GPT-3.5 Turbo
SYSTEM_PROMPT = """You are chatting with an AI. There are no specific prefixes for responses, so you can ask or talk about anything you like.
The AI will respond in a natural, conversational manner. Feel free to start the conversation with any question or topic, and let's have a
pleasant chat!
"""

@bot()
def on_message(message_history: List[Message], state: dict = None):

    # Generate GPT-3.5 Turbo response
    bot_response = OpenAI.generate(
        system_prompt=SYSTEM_PROMPT,
        message_history=message_history, # Assuming history is the list of user messages
        model="gpt-3.5-turbo",
    )

    return {
        "messages": [bot_response],
        "state": state
    }
```

## Bot example for image generation
This particular example uses DALL-E's API. You can use your own or you can even integrate some in the project itself. We are open for contributions!

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

## Bot example for text _and_ image generation
This example uses both OpenAI _and_ DALL-E's API. You can use your own or you can even integrate some in the project itself. We are open for contributions!

**You must import the `Image` datatype and wrap your bot_response with it so that the images can be rendered on the chat UI.**
```py
from typing import List
from textbase import bot, Message
from textbase.models import OpenAI, DallE
from textbase.datatypes import Image

# Load your OpenAI API key
OpenAI.api_key = DallE.api_key = ""

# Prompt for GPT-3.5 Turbo
SYSTEM_PROMPT = """You are chatting with an AI. There are no specific prefixes for responses, so you can ask or talk about anything you like.
The AI will respond in a natural, conversational manner. Feel free to start the conversation with any question or topic, and let's have a
pleasant chat!
"""

@bot()
def on_message(message_history: List[Message], state: dict = None):

    last_message = message_history[-1]['content'][-1]
    data_type = last_message['data_type']

    # Generate GPT-3.5 Turbo response
    if data_type == 'STRING':
        bot_response = OpenAI.generate(
            system_prompt=SYSTEM_PROMPT,
            message_history=message_history, # Assuming history is the list of user messages
            model="gpt-3.5-turbo",
        )

    # Generate similar images based on the image uploaded by the user
    # Note that we are wrapping it around the Image datatype
    elif data_type == 'IMAGE_URL':
        bot_response = Image(DallE.generate_variations(
            message_history=message_history,
            size="1024x1024",
        ))

    return {
        "messages": [bot_response],
        "state": state
    }
```