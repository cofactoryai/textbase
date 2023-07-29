import textbase
from textbase.message import Message
import openai
import os
from typing import List

# Load your OpenAI API key from environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

# Prompt for GPT-3.5 Turbo
GPT3_PROMPT = """You are chatting with an AI. There are no specific prefixes for responses, so you can ask or talk about anything you like. The AI will respond in a natural, conversational manner. Feel free to start the conversation with any question or topic, and let's have a pleasant chat!
"""

@textbase.chatbot("Talking-bot")
def on_message(messages: List[Message], state: dict):
    # Your chatbot logic here
    # messages: List of user messages
    # state: A dictionary to store any stateful information

    # Initialize state if not provided
    if state is None:
        state = {'history': []}

    # Extract the conversation history from the state
    history = state['history']

    # List to store bot response messages
    bot_messages = []

    for message in messages:
        # Prepare the user message as a single string for GPT input
        user_input = f"User: {message.text}"
        full_prompt = f"{GPT3_PROMPT}\n"

        # Append user message to the conversation history
        history.append(user_input)

        # Concatenate the conversation history and user message for GPT input
        for h in history:
            full_prompt += h + "\n"

        # Generate GPT-3.5 Turbo response
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": full_prompt}],
            temperature=0.7,
            max_tokens=3500,
            n=1,
            presence_penalty=0.0,
            frequency_penalty=0.0,
        )

        # Extract the generated response from GPT-3.5 Turbo
        bot_response = response["choices"][0]["message"]["content"].strip()

        # Append the user message and bot response to the conversation history
        history.append(bot_response)

        # Create a message object with the generated response and add it to bot_messages
        bot_message = Message(text=bot_response, sender='bot')
        bot_messages.append(bot_message)

    # Update the conversation history in the state
    state['history'] = history
    # Return the list of bot response messages and updated state
    return bot_messages, state
