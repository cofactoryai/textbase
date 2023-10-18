from typing import List
from textbase import bot, Message
from textbase.models import PalmAI

# Load your PALM API key
PalmAI.api_key = ""

@bot()
def on_message(message_history: List[Message], state: dict = None):

    bot_response = PalmAI.generate(
        message_history=message_history, # Assuming history is the list of user messages
    )

    return {
        "messages": [bot_response],
        "state": state
    }
