import textbase
from textbase.message import Message
from textbase import models
import os
from typing import List

#load your HuggingFace API key
models.HuggingFace.api_key = ""
# or from environment variable:
# models.HuggingFace.api_key = os.getenv("HUGGING_FACE_API_KEY")

# Prompt for the model
SYSTEM_PROMPT = """you are and expert in large language model (llm) field and you will answer accordingly"""


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

    #Generate Hugging face model response
    bot_response = models.HuggingFace.generate(
        system_prompt=SYSTEM_PROMPT,
        message_history=message_history,
        model="jasondubon/HubermanGPT-small-v1"
    )

    return bot_response, state
