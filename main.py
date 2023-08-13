import textbase
from textbase.message import Message
from textbase import models
import os
from typing import List

from dotenv import load_dotenv

load_dotenv()

# Load your OpenAI API key
models.OpenAI.api_key = "YOUR_API_KEY"
# or from environment variable:
models.HuggingFaceHub.api_key = os.getenv("HUGGINGFACEHUB_API_TOKEN")

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

    # Generate GPT-3.5 Turbo response
    bot_response = models.OpenAI.generate(
        system_prompt=SYSTEM_PROMPT,
        message_history=message_history,
        model="gpt-3.5-turbo",
    )
    
    #Generate Hugging face model response using Langchain
    bot_response_new = models.LangchainHuggingFace.generate(
        message_history=message_history,
        system_prompt=SYSTEM_PROMPT,
        model="google/flan-t5-xxl",
        temperature=0.4, 
        top_k=70
    )
    
    return bot_response_new, state