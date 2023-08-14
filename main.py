import textbase
from textbase.message import Message
from textbase import models
import os
from typing import List

# Load your OpenAI API key
models.OpenAI.api_key = "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"

# Health Advisor chatbot logic
@textbase.chatbot("health-bot")
def on_message(message_history: List[Message], state: dict = None):
    if state is None:
        state = {}

    # Get user input from the latest message
    user_input = message_history[-1].content.strip().lower()

    # Check if user input is health-related or a greeting
    is_health_related = health_care_plugin(message_history)
    is_greeting = any(
        word in user_input
        for word in ["hello", "hi", "hey","what","help"]
    )

    # Generate dynamic system prompt based on user messages
    system_prompt = "You are chatting with a Health Advisor. "
    user_messages = [msg.content for msg in message_history if msg.role == "user"]
    if user_messages:
        system_prompt += "User: " + " ".join(user_messages) + " "

    # Generate response using the OpenAI API
    if is_health_related:
        response = models.OpenAI.generate(
            system_prompt=system_prompt,
            message_history=message_history,
            model="gpt-3.5-turbo",
            temperature=0.7,
            max_tokens=100,
        )
    elif is_greeting:
        response = "Hello! I'm here to assist you with health care information and advice."
    else:
        response = "I'm sorry, I can't help you with that. Please try asking me a health-related question."

    bot_response = response.strip()  # Remove extra whitespace

    return bot_response, state

# Health Care plugin logic
def health_care_plugin(message_history: List[Message]) -> bool:
    """Checks if the user input is health-related."""
    user_input = message_history[-1].content.strip().lower()
    return any(
        word in user_input
        for word in ["health", "doctor", "hospital", "symptoms", "medication", "treatment"]
    )

if __name__ == "__main__":
    textbase.run(debug=True)
