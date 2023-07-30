import textbase
from textbase.message import Message
from textbase import models
import os
from typing import List

# Load your OpenAI API key
models.OpenAI.api_key = "YOUR_API_KEY"
# or from environment variable:
# models.OpenAI.api_key = os.getenv("OPENAI_API_KEY")

# Prompt for GPT-3.5 Turbo
SYSTEM_PROMPT = """You are chatting with an AI. There are no specific prefixes for responses, so you can ask or talk about anything you like. The AI will respond in a natural, conversational manner. Feel free to start the conversation with any question or topic, and let's have a pleasant chat!
"""

# Modified Prompt for fair chatbot that also has movie recommendation and flight detail capabilities
MOD_PROMPT = """You are chatting with an AI. There are no specific prefixes for responses, so you can ask or talk about anything you like. 
The AI will respond in a natural, conversational manner, but gives short crisp replies, and has no bias or discrimination towards gender, race, religion. Feel free to start the conversation with any question or topic, 
and let's have a pleasant chat! If the AI does not know the answer it should state that and not try to hallucinate answers. The AI is also a movie recommender and flight information guide!
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
    # bot_response = models.OpenAI.generate(
    #     system_prompt=SYSTEM_PROMPT,
    #     message_history=message_history,
    #     model="gpt-3.5-turbo",
    # )

    # Using custom function to integrate the functionalities also based on OpenAI
    bot_response = models.OpenAI.movie_flight(
        system_prompt=MOD_PROMPT,
        message_history=message_history,
        model="gpt-3.5-turbo",
    )

    return bot_response, state
