from textbase import bot, Message
from textbase.models import HuggingFace
from typing import List

# Load your HuggingFace API key
HuggingFace.api_key = ""

# Define a dictionary to map emotions to emojis
EMOJI_MAP = {
    "happy": "😄",
    "sad": "😢",
    "angry": "😡",
    # Add more emotions and emojis as needed
}

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

    # Detect emotion in the bot's response (you can replace this with a real emotion detection method)
    detected_emotion = "happy"  # For example, let's assume the bot is happy

    # Get the corresponding emoji for the detected emotion
    emoji = EMOJI_MAP.get(detected_emotion, "😐")  # Default to a neutral emoji if no emotion is detected

    # Add the emoji to the bot's response
    bot_response_with_emoji = f"{emoji} {bot_response}"

    response = {
        "data": {
            "messages": [
                {
                    "data_type": "STRING",
                    "value": bot_response_with_emoji
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
