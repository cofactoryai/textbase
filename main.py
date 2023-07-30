import textbase
from textbase.message import Message
from textbase import models
import os
from typing import List
import speech_recognition as sr
import pyttsx3
import emoji
from PIL import Image
from io import BytesIO
from googletrans import Translator
import hashlib

# Load your OpenAI API key
models.OpenAI.api_key = "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"
# or from environment variable:
# models.OpenAI.api_key = os.getenv("OPENAI_API_KEY")

# Prompt for GPT-3.5 Turbo
SYSTEM_PROMPT = """You are chatting with an AI. There are no specific prefixes for responses, so you can ask or talk about anything you like. The AI will respond in a natural, conversational manner. Feel free to start the conversation with any question or topic, and let's have a pleasant chat!
"""
# Personality options
PERSONALITY_OPTIONS = ["friendly", "formal", "humorous"]

# Mapping of client IDs to their chosen personalities
client_personalities = {}

# Initialize the speech recognizer
recognizer = sr.Recognizer()

# Initialize the text-to-speech engine
tts_engine = pyttsx3.init()

# Initialize language translator
translator = Translator()

def speak(text):
    tts_engine.say(text)
    tts_engine.runAndWait()


def recognize_speech():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        return text
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand your voice.")
        return None
    except sr.RequestError:
        print("There was an issue with the speech recognition service.")
        return None

def recognize_image(image_url):
    try:
        # Fetch the image from the provided URL
        # You can use libraries like `requests` or `urllib` to fetch the image from the URL.
        image = Image.open(BytesIO(image_data))

        # Implement image recognition logic to analyze the image and extract relevant information.
        # For simplicity, we'll just return a generic response here.
        return "I see an interesting image! Unfortunately, I'm not equipped to analyze images in detail yet."
    except Exception as e:
        print("Error processing the image:", str(e))
        return "Oops! There was an issue processing the image. Please try again."

def get_client_id(user_ip):
    # Use the user's IP address as a unique identifier for the client_id
    # You can modify this method to generate client_id based on your requirements.
    # For simplicity, we use hashlib to hash the user's IP address.
    return hashlib.sha256(user_ip.encode()).hexdigest()

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

    # Retrieve the latest user message from message_history
    user_input = message_history[-1].content

    # Get the user's IP address (simulated for demonstration purposes)
    user_ip = "192.168.1.1"  # Simulated IP address, replace with actual user IP address.

    # Get the client ID using the user's IP address
    client_id = get_client_id(user_ip)

    # Check if the client has selected a personality
    if client_id not in client_personalities:
        client_personalities[client_id] = "friendly"  # Default to "friendly" personality

    # Get the client's chosen personality
    client_personality = client_personalities[client_id]

    # If user input is 'voice', enable voice input
    if user_input.strip().lower() == 'voice':
        user_input = recognize_speech()
        if not user_input:
            # In case of voice recognition failure, return an empty response
            return "", state

    
    # If user input contains an image URL, process the image
    if user_input.startswith("image:"):
        image_url = user_input.split(":", 1)[1].strip()
        response = recognize_image(image_url)
        return response, state

    # If user input contains an emoji, process the emoji
    if any(char in emoji.UNICODE_EMOJI for char in user_input):
        # Implement emoji recognition logic to understand the meaning of the emoji.
        # For simplicity, we'll just return a generic response here.
        response = "You sent an emoji! 😄"
        return response, state
    
    # If user input is 'translate', enable language translation
    if user_input.strip().lower() == 'translate':
        return "Please provide the text you want to translate.", state

    # If the user provided text for translation, proceed with language translation
    if state.get("translate_mode"):
        detected_lang = translator.detect(user_input).lang
        translated_text = translator.translate(user_input, src=detected_lang, dest='en').text

        # Reset translate mode
        state["translate_mode"] = False
        return f"Translated to English: {translated_text}", state
    
    # # # Generate GPT-3.5 Turbo response
    # bot_response = models.OpenAI.generate(
    #     system_prompt=SYSTEM_PROMPT,
    #     message_history=message_history,
    #     model="gpt-3.5-turbo",
    # )

    # Implement different responses based on the selected personality
    if client_personality == "friendly":
        bot_response = models.OpenAI.generate(
            system_prompt=SYSTEM_PROMPT,
            message_history=message_history,
            model="gpt-3.5-turbo",
        )
    elif client_personality == "formal":
        bot_response = "Greetings. How may I be of service to you?"
    elif client_personality == "humorous":
        bot_response = "Why did the chicken cross the road? To get to the other side! 😄"

    # If user input was 'voice', enable voice output
    if user_input.strip().lower() == 'speak':
        speak(bot_response)
        return "", state

    return bot_response, state
