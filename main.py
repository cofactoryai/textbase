import textbase
from textbase.message import Message
import openai
import os
from typing import List

# Load your OpenAI API key from environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

# Prompt for GPT-3.5 Turbo
GPT3_PROMPT = """You are a helpful chatbot whose responsibility is to reply to the user with a genuine message according to what they ask.

You can start the conversation with a user message, and the chatbot will provide an appropriate response.
Give the response to user's questions as is, do not include any extra prefix like Chatbot: or Assistant:
"""

@textbase.chatbot("cologne-bot")
def on_message(messages: List[Message], state: dict):
    # Your chatbot logic here
    # messages: List of user messages
    # state: A dictionary to store any stateful information

    # Initialize state if not provided
    if state is None:
        state = {}

    # List to store bot response messages
    bot_messages = []

    for message in messages:
        # Prepare the user message as a single string for GPT input
        user_input = f"User: {message.text}"
        full_prompt = f"{GPT3_PROMPT}\n{user_input}\n"

        # Generate GPT-3.5 Turbo response
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": full_prompt}, {"role": "user", "content": user_input}],
            temperature=0.7,
            max_tokens=3500,
            n=1,
            presence_penalty=0.0,
            frequency_penalty=0.0,
        )

        # Extract the generated response from GPT-3.5 Turbo
        bot_response = response["choices"][0]["message"]["content"].strip()

        # Create a message object with the generated response and add it to bot_messages
        bot_message = Message(text=bot_response, sender='bot')
        bot_messages.append(bot_message)

    # Return the list of bot response messages
    return bot_messages, state
