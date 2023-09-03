from textbase import bot, Message
from textbase.models import OpenAI
from typing import List

# Load your OpenAI API key
OpenAI.api_key = "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"

# Prompt for GPT-3.5 Turbo
SYSTEM_PROMPT = """You are chatting with an AI. There are no specific prefixes for responses, so you can ask or talk about anything you like.
The AI will respond in a natural, conversational manner. Feel free to start the conversation with any question or topic, and let's have a
pleasant chat!
"""

@bot()
def on_message(message_history: List[Message], state: dict = None):

    prompt_check = ['photo','image','picture']
    flag = 0
    print(message_history)
    # Generate GPT-3.5 Turbo response
    for prompt in prompt_check:
        if prompt in message_history[len(message_history)-1]['content'][0]['value']:
            flag = 1
            bot_response = OpenAI.image_generate(
            system_prompt=SYSTEM_PROMPT,
            message_history=message_history, # Assuming history is the list of user messages
            model="gpt-3.5-turbo",
            )
            break
    if flag != 1:
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