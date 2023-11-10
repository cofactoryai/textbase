---
sidebar_position: 7
---

# GPT Assistants bot
This bot calls Vision API from OpenAI and processes the user image.

```py
from typing import List
from textbase import bot, Message
from textbase.models import OpenAI

# Load your OpenAI API key
OpenAI.api_key = ""

@bot()
def on_message(message_history: List[Message], state: dict = None):
    last_message = message_history[-1]['content'][-1]
    text = last_message['value']

    if ('id' not in state):
        state['id'] = OpenAI.create_assistant(
            name="Math Tutor",
            instructions="You are a personal math tutor. Write and run code to answer math questions.",
            tools=[{"type": "code_interpreter"}],
            model="gpt-4-1106-preview"
        )

    while(state['id'] != ''):
        bot_responses = OpenAI.run_assistant(
            message_history=message_history,
            text=text,
            assistant_id=state['id']
        )

        return {
            "messages": [bot_responses],
            "state": state
        }
```