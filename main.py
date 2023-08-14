import textbase
from textbase.message import Message
from textbase import models
import os
from typing import List
import difflib

# Load your OpenAI API key
models.OpenAI.api_key =""

# Read health keywords from the file
with open("health_keywords.txt", "r") as file:
    all_keywords = [line.strip() for line in file]

# User profiles dictionary to store user data
user_profiles = {}

# Health Advisor chatbot logic
@textbase.chatbot("health-bot")
def on_message(message_history: List[Message], state: dict = None):
    if state is None:
        state = {}

    # Get user input from the latest message
    user_input = message_history[-1].content.strip().lower()

    # Check if user input is health-related
    is_health_related = health_care_plugin(user_input)

    # Generate dynamic system prompt based on user messages
    system_prompt = "You are chatting with a Health Advisor. "
    user_messages = [msg.content for msg in message_history if msg.role == "user"]
    if user_messages:
        system_prompt += "User: " + " ".join(user_messages) + " "

    # If the input is a common greeting, provide a prompt to ask something related to healthcare
    if any(greeting in user_input for greeting in ["hello", "hi", "hey", "how are you", "suffering"]):
        bot_response = "Hello! Feel free to ask me any health-related questions or share your healthcare concerns."
    elif is_health_related:
        response = models.OpenAI.generate(
            system_prompt=system_prompt,
            message_history=message_history,
            model="gpt-3.5-turbo",
            temperature=0.7,
            max_tokens=100,
        )
        bot_response = response.strip()  # Remove extra whitespace
    else:
        bot_response = "I'm sorry, I can't help you with that. Please try asking me a health-related question."

    return bot_response, state

# Health Care plugin logic
def health_care_plugin(user_input: str) -> bool:
    """Checks if the user input is health-related."""
    return any(
        word in user_input
        for word in all_keywords
    ) or any(
        difflib.get_close_matches(word, all_keywords)
        for word in user_input.split()  # Check each word individually
    )

# User profile creation function
def create_user_profile(name, contact_details, medical_history):
    user_profiles[name] = {
        "contact_details": contact_details,
        "medical_history": medical_history
    }

def interact_with_chatbot():
    name = input("Enter your name: ")
    contact_details = input("Enter your contact details: ")
    medical_history = input("Enter your medical history: ")
    create_user_profile(name, contact_details, medical_history)

    while True:
        user_input = input("You: ")
        is_health_related = health_care_plugin(user_input)

        if any(greeting in user_input for greeting in ["hello", "hi", "hey", "how are you"]):
            bot_response = "Hello! Feel free to ask me any health-related questions or share your healthcare concerns."
        elif is_health_related:
            response = models.OpenAI.generate(
                system_prompt="You are chatting with a Health Advisor. User: " + user_input,
                message_history=[Message(content=user_input, role="user")],
                model="gpt-3.5-turbo",
                temperature=0.7,
                max_tokens=100,
            )
            bot_response = response.choices[0].text.strip()
        else:
            bot_response = "I'm sorry, I can't help you with that. Please try asking me a health-related question."

        print("Bot:", bot_response)

if __name__ == "__main__":
    interact_with_chatbot()
