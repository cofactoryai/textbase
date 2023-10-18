from typing import List
from textbase import bot, Message
from textbase.models import HuggingFace

# Load your HuggingFace API key
HuggingFace.api_key = ""

# Prompt for GPT-3.5 Turbo
SYSTEM_PROMPT = """You are chatting with an AI. There are no specific prefixes for responses, so you can ask or talk about anything you like.
The AI will respond in a natural, conversational manner. Feel free to start the conversation with any question or topic, and let's have a
pleasant chat!
"""

@bot()
def on_message(message_history: List[Message], state: dict = None):

    # Generate HuggingFace response. Uses the DialoGPT-large model from Microsoft by default.
    bot_response = HuggingFace.generate(
        system_prompt=SYSTEM_PROMPT,
        message_history=message_history, # Assuming history is the list of user messages
    )

    return {
        "messages": [bot_response],
        "state": state
    }