---
sidebar_position: 4
---

# LangChain bot

This bot is built on top of the OpenAI bot. It uses LangChain to provide integrations with multiple services such as Google search, Wikipedia to name a few. The complete list of supported integrations are available [here](https://python.langchain.com/docs/integrations/tools/). 

By default the bot uses GPT-3.5 Turbo and is configured with `wikipedia`, `llm-math` and `serpapi` integrations.

```py
from textbase import bot, Message
from textbase.models import LangChain
from typing import List

# Load your OpenAI API key
LangChain.open_ai_api_key = "YOU OPENAI API KEY"
LangChain.api_keys = { 
    'SERPAPI_API_KEY': "YOUR SERPAPI API KEY"
}

# Prompt for GPT-3.5 Turbo
SYSTEM_PROMPT = """You are chatting with an AI. There are no specific prefixes for responses, so you can ask or talk about anything you like.
The AI will respond in a natural, conversational manner. Feel free to start the conversation with any question or topic, and let's have a
pleasant chat!
"""

@bot()
def on_message(message_history: List[Message], state: dict = None):

    # Generate GPT-3.5 Turbo response with integrations
    bot_response = LangChain.generate(
        system_prompt=SYSTEM_PROMPT,
        message_history=message_history, # Assuming history is the list of user messages
        model="gpt-3.5-turbo",
        max_tokens=1000,
        temperature=0.25,
        max_iterations=5,
        tools=['serpapi', 'wikipedia', 'llm-math'],
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

<br />

# Limitations of the bot

1. The bot doesn't remember the context of the conversation as of now.
2. You can only ask questions to the bot else it will respond with a `N/A` message.
3. The bot can't respond to descriptive questions as of now.