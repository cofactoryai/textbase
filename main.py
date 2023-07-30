import textbase
from textbase.message import Message
from textbase import models
import os
from typing import List
import json

# Load your OpenAI API key
# models.OpenAI.api_key = "YOUR_API_KEY_HERE"
# or from environment variable:
models.OpenAI.api_key = os.getenv("OPENAI_API_KEY")

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

    return bot_response, state

@textbase.chatbot("talking-bot")
def on_message_edge(message_history: Message):
    bot_response = models.OpenAI.generate_using_Edge(
        system_prompt=SYSTEM_PROMPT,
        message_history=message_history,
    )
    return bot_response

# @textbase.chatbot("talking-bot")
# def on_message_image(message_history: Message):
#     bot_response = models.OpenAI.generate_image_using_Edge(
#         system_prompt=SYSTEM_PROMPT,
#         message_history=message_history,
#     )
#     return bot_response

@textbase.chatbot("talking-bot")
def on_message_analyse(message_history: Message):
    bot_response = models.OpenAI.analyse_text_recognant(
        system_prompt=SYSTEM_PROMPT,
        message_history=message_history,
    )
    return bot_response