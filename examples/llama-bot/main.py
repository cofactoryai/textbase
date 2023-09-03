from textbase import bot, Message
from textbase.models import Llama
from typing import List

# Load your Replicate API key
Llama.replicate_api_key = ""

# Prompt for Llama7b. Llama gets offensive with larger complicated system prompts. This works just fine
SYSTEM_PROMPT = """\
You are a helpful assistant"""

@bot()
def on_message(message_history: List[Message], state: dict = None):

    # Generate Llama7b response by default
    bot_response = Llama.generate(
        system_prompt=SYSTEM_PROMPT,
        message_history=message_history, # Assuming history is the list of user messages
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