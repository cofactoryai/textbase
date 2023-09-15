from textbase import bot, Message
from textbase.models import LangChain
from typing import List

# Load your OpenAI API key
LangChain.open_ai_api_key = "YOUR OPENAI API KEY"
LangChain.api_keys = { 
    'SERPAPI_API_KEY': "YOUR SERPAPI API KEY",
}

# Set the memory window size for LangChain
LangChain.memory.k = 6 # Default value is 6

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