import textbase
from textbase.message import Message
from textbase import models
from typing import List
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import pipeline

# Load your OpenAI API key
models.OpenAI.api_key = "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"
# or from environment variable:
# models.OpenAI.api_key = os.getenv("OPENAI_API_KEY")

input_variable = "Indian Penal Code" # You can change whatever the chatbot to act like

# Prompt for GPT-3.5 Turbo
SYSTEM_PROMPT = """You are chatting with an AI. There are no specific prefixes for responses, so you can ask or talk about anything you like. The AI will respond in a natural, conversational manner. Feel free to start the conversation with any question or topic, and let's have a pleasant chat!

If your input is related to the {}, I will provide you with sections and a detailed overview of the topics related to {}. Otherwise, I will respond with a plain NO.
""".format(input_variable, input_variable)

# Create the sentiment analysis analyzer
sentiment_analyzer = SentimentIntensityAnalyzer()

# Function to perform sentiment analysis
def analyze_sentiment(text: str) -> str:
    # Calculate the sentiment score using VADER
    sentiment_score = sentiment_analyzer.polarity_scores(text)
    
    # VADER provides a compound score ranging from -1 (most negative) to 1 (most positive)
    compound_score = sentiment_score["compound"]

    # Classify sentiment based on the compound score
    if compound_score >= 0.05:
        return "positive"
    elif compound_score > -0.05 and compound_score < 0.05:
        return "neutral"
    else:
        return "negative"
    
# Function to check if the input is related to the Indian Penal Code
def is_related_to_input_variable(text: str) -> bool:
    # Implement your logic here to determine if the input is related to the Indian Penal Code
    # You can use any NLP techniques or pattern matching to identify relevant keywords
    ipc_keywords = ["Indian Penal Code", "IPC", "criminal law", "crime", "section"] #you can add whever words to identify
    return any(keyword in text for keyword in ipc_keywords)

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

    user_input = message_history[-1].content

    # Step 1: Sentiment Analysis
    sentiment = analyze_sentiment(user_input)

    if sentiment == "positive" or sentiment == "neutral" :
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
