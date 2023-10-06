from textbase import bot, Message
from textbase.models import DallE
from typing import List
import click
from textbase.classes import image

# Load your OpenAI API key
DallE.api_key = ""

@bot()
def on_message(message_history: List[Message], state: dict = None):

    # Generate DallE response
    try:
        bot_response = DallE.generate(
            message_history=message_history, # Assuming history is the list of user messages
        )
    except Exception as e :
        click.secho(str(e.with_traceback(e.__traceback__)), fg='red')
        return {
            "messages": [],
            "state": state,
            "errors": [str(e)]
        }

    return {
        "messages": [image(bot_response)],
        "state": state
    }
