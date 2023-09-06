from textbase import bot, Message
from textbase.models import OpenAI
from typing import List

# Load your OpenAI API key
OpenAI.api_key = ""

# Prompt for GPT-3.5 Turbo
SYSTEM_PROMPT = """You are an elocution and pronunciation tutor. Your goal is to help users improve their speech and pronunciation by focusing on syllable sounds.
Please provide clear explanations and examples to help users understand and practice the correct pronunciation of words with different syllable structures.
Also encourage users to ask questions and engage in pronunciation exercises with you.
"""

@bot()
def on_message(message_history: List[Message], state: dict = None):

    # Generate GPT-3.5 Turbo response
    bot_response = OpenAI.generate(
        system_prompt=SYSTEM_PROMPT,
        message_history=message_history, # Assuming history is the list of user messages
        model="gpt-3.5-turbo",
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