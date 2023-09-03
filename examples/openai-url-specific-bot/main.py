from textbase import bot, Message
from textbase.models import OpenAI
from typing import List
import requests
from bs4 import BeautifulSoup

# # Load your OpenAI API key
OpenAI.api_key = ""
urls = []  # Add list of URLs to train on

def extract_text_from_urls(urls, max_words=1000):
    text_data = []

    for url in urls:
        try:
            response = requests.get(url)
            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                page_text = soup.get_text()
                words = page_text.split()
                truncated_text = ' '.join(words[:max_words])
                text_data.append(truncated_text)
            else:
                print(
                    f"Failed to fetch URL: {url}. Status code: {response.status_code}")
        except Exception as e:
            print(f"Error fetching URL: {url}. Error: {str(e)}")
    return text_data


# Prompt for GPT-3.5 Turbo
SYSTEM_PROMPT = "This is the data for you to train. Questions will be asked on this - " + \
    "\n".join(extract_text_from_urls(urls, max_words=1000))


@bot()
def on_message(message_history: List[Message], state: dict = None):

    # Generate GPT-3.5 Turbo response
    bot_response = OpenAI.generate(
        system_prompt=SYSTEM_PROMPT,
        message_history=message_history,  # Assuming history is the list of user messages
        model="gpt-3.5-turbo",
    )

    response = {
        "data": {
            "messages": [
                {
                    "data_type": "STRING",
                    "value": bot_response
                }
            ],
            "state": state
        },
        "errors": [
            {
                "message": ""
            }
        ]
    }

    return {
        "status_code": 200,
        "response": response
    }