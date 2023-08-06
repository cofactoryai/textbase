import textbase
from textbase.message import Message
from textbase import models
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import pipeline
from typing import List

# Load your OpenAI API key
models.OpenAI.api_key = "YOUR_API_KEY"
# or from environment variable:
# models.OpenAI.api_key = os.getenv("OPENAI_API_KEY")

input_variable = "Indian Penal Code"  # You can change whatever the chatbot to act like

# Prompt for GPT-3.5 Turbo
SYSTEM_PROMPT = f"""You are chatting with an AI. There are no specific prefixes for responses, so you can ask or talk about anything you like. The AI will respond in a natural, conversational manner. Feel free to start the conversation with any question or topic, and let's have a pleasant chat!

If your input is related to the {input_variable}, I will provide you with sections and a detailed overview of the topics related to {input_variable}. Otherwise, I will respond with a plain NO.
"""

# Create the sentiment analysis analyzer
sentiment_analyzer = SentimentIntensityAnalyzer()

# Function to perform sentiment analysis
def analyze_sentiment(text: str) -> str:
    sentiment_score = sentiment_analyzer.polarity_scores(text)
    compound_score = sentiment_score["compound"]

    if compound_score >= 0.1:
        return "positive"
    elif -0.1 < compound_score < 0.1:
        return "neutral"
    else:
        return "negative"

# Function to check if the input is related to the Indian Penal Code
def is_related_to_input_variable(text: str) -> bool:
    ipc_keywords = ["Indian Penal Code", "IPC", "criminal law", "crime", "section"]
    return any(keyword in text for keyword in ipc_keywords)

@textbase.chatbot("talking-bot")
def on_message(message_history: List[Message], state: dict = None):
    if state is None:
        state = {"counter": 0}
    else:
        state["counter"] = state.get("counter", 0) + 1

    user_input = message_history[-1].content

    # Step 1: Sentiment Analysis
    sentiment = analyze_sentiment(user_input)

    if sentiment == "positive" or sentiment == "neutral":
        # Positive input, check if related to the Indian Penal Code
        if is_related_to_input_variable(user_input):
            # If related, use GPT-3.5 Turbo with prompt for sections and detailed overview
            bot_response = models.OpenAI.generate(
                system_prompt=SYSTEM_PROMPT + "\nUser: " + user_input,
                message_history=message_history,
                model="gpt-3.5-turbo",
            )
        else:
            # If not related to IPC, respond with plain NO and ask for legal related text
            bot_response = "NO\nPlease provide a legal-related text as a response."
    else:
        # Negative input, ask for more information or provide guidance
        bot_response = "I'm sorry you're feeling this way. Can you please provide more information or rephrase your input?"

    return bot_response, state
