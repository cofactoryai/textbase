from textbase import bot, Message
from textbase.models import OpenAI
from typing import List

# Load your OpenAI API key
OpenAI.api_key = ""

# Prompt for GPT-3.5 Turbo
SYSTEM_PROMPT = """You are using a task management AI. You can provide a list of tasks, and I'll help you arrange them by priority.
Please enter your tasks, one at a time, and assign a priority level from 1 to 5 to each task, where 1 is the highest priority and 5 is the lowest. For example:
- Task: Complete the report (Priority: 1)
- Task: Buy groceries (Priority: 3)
Feel free to add as many tasks as you'd like, and I'll sort them for you. You can also ask for a sorted list at any time by saying 'Sort my tasks.'
Let's get organized!
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
