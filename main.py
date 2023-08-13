import textbase
from textbase.message import Message
from textbase import models
import os
from typing import List
import json
import requests

# Load your HuggingFace API key
models.HuggingFace.api_key = "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"
# or load from an environment variable:
# models.HuggingFace.api_key = os.getenv("HUGGING_FACE_API_KEY")

# Prompt for the model
SYSTEM_PROMPT = """you are an expert in the large language model (LLM) field and you will answer accordingly"""

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

    try:
        assert models.HuggingFace.api_key is not None, "Hugging Face API key is not set"

        headers = {"Authorization": f"Bearer {models.HuggingFace.api_key}"}
        API_URL = "https://api-inference.huggingface.co/models/gpt-3.5-turbo"

        inputs = {
            "past_user_inputs": [SYSTEM_PROMPT],
            "generated_responses": [],
            "text": ""
        }

        for message in message_history:
            if message.role == "user":
                inputs["past_user_inputs"].append(message.content)
            else:
                inputs["generated_responses"].append(message.content)

        inputs["text"] = inputs["past_user_inputs"].pop(-1)
        payload = {
            "inputs": inputs,
            "max_length": 3000,
            "temperature": 0.7,
        }
        data = json.dumps(payload)
        response = requests.request("POST", API_URL, headers=headers, data=data)
        response = json.loads(response.content.decode("utf-8"))

        bot_response = response["generated_text"]
        return bot_response, state

    except Exception as ex:
        error_message = f"Error: {ex}"
        return error_message, state
