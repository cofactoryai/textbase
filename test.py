# test_registration.py

from textbase import registered_chatbots
from textbase.chatbot import TestChatbot

# List all registered chatbot names
print("Registered Chatbots:")
for name in registered_chatbots:
    print("-", name)

# Create an instance of the TestChatbot
chatbot = TestChatbot('cologne-chatbot')

# Test the chatbot with different user messages
user_messages = [
    "Hi, how are you?",
    "I wanted to know if there's a way to book cheaper flights",
    "What's the weather like today?",
]

print("\nChatbot Responses:")
for message in user_messages:
    response = chatbot.process_message(message)
    print(response)
