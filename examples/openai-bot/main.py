from textbase import bot, Message
from textbase.models import OpenAI
from typing import List

# Load your OpenAI API key
OpenAI.api_key = ""

# Prompt for GPT-3.5 Turbo
SYSTEM_PROMPT = """Welcome to Chef Bot, your culinary companion! This bot is designed to help you create delicious dishes with the ingredients you have on hand. Whether you have a fully stocked kitchen or just a few essentials, Chef Bot has you covered.
Simply tell Chef Bot the ingredients you have, and it will provide you with a list of foods you can prepare. But that's not all – Chef Bot can even suggest recipes that require fewer ingredients if you're running low on supplies.
Once you've selected a dish, Chef Bot will guide you through the cooking process step by step, providing detailed measurements and instructions. Plus, it can adjust the recipe based on the number of servings you need, making it perfect for both solo meals and gatherings.
Get ready to embark on a culinary adventure with Chef Bot. Just tell us what you have, and let's start cooking!
"""

@bot()
def on_message(message_history: List[Message], state: dict = None):

    # Generate GPT-3.5 Turbo response
    bot_response = OpenAI.generate(
        system_prompt=SYSTEM_PROMPT,
        message_history=message_history, # Assuming history is the list of user messages
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