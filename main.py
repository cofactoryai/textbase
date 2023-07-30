import textbase
from textbase.message import Message
from textbase import models
import os
from typing import List

# Load your OpenAI API key
models.OpenAI.api_key = "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"
# or from environment variable:
# models.OpenAI.api_key = os.getenv("OPENAI_API_KEY")

# Prompt for GPT-3.5 Turbo
# SYSTEM_PROMPT = """You are chatting with an AI. There are no specific prefixes for responses, so you can ask or talk about anything you like. The AI will respond in a natural, conversational manner. Feel free to start the conversation with any question or topic, and let's have a pleasant chat!
SYSTEM_PROMPT = """You are chatting with a Job Interview Preparation Chatbot. \
        First greet student with offering your service, then proceed.\
        This chatbot is designed to help you improve your interview skills and provide tips to boost your confidence. \
    Keep in mind that while the chatbot can offer valuable advice, practice and preparation are essential for a successful interview.\
        Please remember that the chatbot cannot predict specific interview questions or guarantee \
    the outcome of your interviews. However, it can provide general guidance and best practices.\
        When student tells the domain of interview then ask him that does he need mock interview or general tips.\
        If user chooses to mock interview then ask 5-10 questions about the domain provided and in the end provide a \
    feedback on students answers.\
    """

@textbase.chatbot("talking-bot")
def on_message(message_history: List[Message], state: dict = None):
    """Your chatbot logic here
    message_history: List of user messages
    state: A dictionary to store any stateful information

    Return a string with the bot_response or a tuple of (bot_response: str, new_state: dict)
    """

     # Extract the latest user message
    user_input = message_history[-1].content.strip().lower()

    if state is None or "counter" not in state:
        state = {"counter": 0}
    else:
        state["counter"] += 1


    # Function Calling: Support specific commands
    if user_input == "help":
        bot_response = "Sure! You can ask me anything, and I'll do my best to assist you."
    elif user_input in ["interview tips", "tips"]:
        bot_response = "To prepare for your job interview, research the company, practice technical questions, and work on your communication skills."
    else:
        # # Generate GPT-3.5 Turbo response
        bot_response = models.OpenAI.generate(
            system_prompt=SYSTEM_PROMPT,
            message_history=message_history,
            model="gpt-3.5-turbo",
        )

    return bot_response, state
