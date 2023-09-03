import os
from textbase import bot, Message
from textbase.models import OpenAI
from typing import List

# Load your OpenAI API key
# OpenAI.api_key = ""
# or from environment variable:
OpenAI.api_key = os.getenv("OPENAI_API_KEY")

# Prompt for GPT-3.5 Turbo
SYSTEM_PROMPT = "You are reviewing a codebase and have identified some mistakes. Please explain the mistakes you've found in the code and provide solutions for each. You can focus on code quality, best practices, performance, or any other relevant aspects. Be thorough and provide clear explanations to help the developer understand and improve the code."

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