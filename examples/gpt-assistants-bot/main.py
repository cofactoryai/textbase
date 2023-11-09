from typing import List
from textbase import bot, Message
import openai
from textbase.models import OpenAI
import time

# Load your OpenAI API key
OpenAI.api_key = ""

# Prompt for GPT-3.5 Turbo
SYSTEM_PROMPT = """You are chatting with an AI. There are no specific prefixes for responses, so you can ask or talk about anything you like.
The AI will respond in a natural, conversational manner. Feel free to start the conversation with any question or topic, and let's have a
pleasant chat!
"""

@bot()
def on_message(message_history: List[Message], state: dict = None):
    last_message = message_history[-1]['content'][-1]
    text = last_message['value']

    bot_responses = OpenAI.assistants(
        message_history=message_history,
        text=text
    )

    return {
        "messages": [bot_responses],
        "state": state
    }
