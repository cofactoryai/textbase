import textbase
from textbase.message import Message
from textbase import models
import os
from typing import List
from twilio.twiml.messaging_response import MessagingResponse
from flask import Flask, request

# Load your OpenAI API key
models.OpenAI.api_key = "YOUR_API_KEY"
# or from environment variable:
# models.OpenAI.api_key = os.getenv("OPENAI_API_KEY")

# Twilio credentials
TWILIO_ACCOUNT_SID = "YOUR_TWILIO_ACCOUNT_SID"
TWILIO_AUTH_TOKEN = "YOUR_TWILIO_AUTH_TOKEN"
TWILIO_PHONE_NUMBER = "YOUR_TWILIO_PHONE_NUMBER"  # Your Twilio phone number

app = Flask(__name__)

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

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    incoming_message = request.form.get('Body', '').lower()
    response, state = on_message([Message(content=incoming_message)], state=None)

    twilio_response = MessagingResponse()
    twilio_response.message(response)

    return str(twilio_response)

@app.route('/sms', methods=['POST'])
def handle_sms():
    incoming_message = request.form.get('Body', '').lower()
    response, state = on_message([Message(content=incoming_message)], state=None)

    twilio_response = MessagingResponse()
    twilio_response.message(response)

    return str(twilio_response)

if __name__ == '__main__':
    app.run(debug=True)
