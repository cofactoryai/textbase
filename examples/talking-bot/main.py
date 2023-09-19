from textbase import bot, Message
from textbase.models import OpenAI
from typing import List
import os
import pyttsx3

# Load your OpenAI API key
OpenAI.api_key = os.getenv("OPENAI_API_KEY")
#Flags to control tts in request/response
user_request_tts = os.getenv("USER_REQUEST_TTS")
bot_response_tts = os.getenv("BOT_RESPONSE_TTS")

# Prompt for GPT-3.5 Turbo
SYSTEM_PROMPT = """You are chatting with an AI. There are no specific prefixes for responses, so you can ask or talk about anything you like.
The AI will respond in a natural, conversational manner. Feel free to start the conversation with any question or topic, and let's have a
pleasant chat!
"""

@bot()
def on_message(message_history: List[Message], state: dict = None):

    # Generate GPT-3.5 Turbo response
    bot_response = OpenAI.generate(
        system_prompt=SYSTEM_PROMPT,
        message_history=message_history, # Assuming history is the list of user messages
        model="gpt-3.5-turbo",
    )
    if user_request_tts == "True":
        textToSpeech(message_history[-1]["content"][0]["value"]) #Speak out User request
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
    if bot_response_tts == "True":
        textToSpeech(bot_response)  #Speak out bot response

    return {
        "status_code": 200,
        "response": response
    }

#Text-to-speech converter
def textToSpeech(response):
    pytts = pyttsx3.init()
    pytts.say(response)
    pytts.runAndWait()