import pyttsx3
import speech_recognition as sr
import textbase
from textbase.message import Message
from textbase import models
import os
from typing import List

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
print(voices[0].id)
engine.setProperty('voices',voices[0].id)



def speak(audio):
    engine.say(audio)
    engine.runAndWait()


# AI introduction at the start
def intro():
    introduction = "Hello, My name is Friday, I am your virtual host"
    speak(introduction)
    ask = "How can I help you, you can ask me anyting"
    speak(ask)

# Take continous input In every 5 seconds 
def takeCommand():
    print("please say after 5 second:::::::")
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        query = r.recognize_google(audio,language='en-in')

    except Exception as e:
        s = "can you say that again please i could not here..."
        speak(s)
        return "none"
    return query



# Load your OpenAI API key
models.OpenAI.api_key = "YOUR_API_KEY"
# or from environment variable:
# models.OpenAI.api_key = os.getenv("OPENAI_API_KEY")

# Prompt for GPT-3.5 Turbo
SYSTEM_PROMPT = """You are chatting with an AI. There are no specific prefixes for responses, so you can ask or talk about anything you like. The AI will respond in a natural, conversational manner. Feel free to start the conversation with any question or topic, and let's have a pleasant chat!
"""


@textbase.chatbot("talking-bot")
def on_message(message_history: List[Message], state: dict = None):
    """Your chatbot logic here
    message_history: List of user messages
    state: A dictionary to store any stateful information

    Return a string with the bot_response or a tuple of (bot_response: str, new_state: dict)
    """

    if state is None or "counter" not in state:
        state = {"counter": 0}
    else:
        state["counter"] += 1

# # Generate GPT-3.5 Turbo response
    bot_response = models.OpenAI.generate(
        system_prompt=SYSTEM_PROMPT,
        message_history=message_history,
        model="gpt-3.5-turbo",
    )

    speak(bot_response)

    return bot_response, state



if __name__ == '__main__': 
    intro()
    while True:
        query = takeCommand().lower()
        on_message([query])
