import textbase
from textbase.message import Message

@textbase.chatbot("cologne-bot")
def on_message(messages: list[Message], state: dict):
    # Your chatbot logic here
    # messages: List of user messages
    # state: A dictionary to store any stateful information

    # For demonstration purposes, we'll just echo back the user messages
    new_messages = [Message(text=message.text, sender='bot') for message in messages]

    return new_messages, state