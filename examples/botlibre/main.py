import textbase
from textbase.message import Message
from textbase import models
from typing import List

# Load your Botlibre Application and Instance
models.BotLibre.application = "YOUR_APPLICATION_ID"
models.BotLibre.instance = "YOUR_INSTANCE_ID"

@textbase.chatbot("talking-bot")
def on_message(message_history: List[Message], state: dict = None):
    output = models.BotLibre.generate(message_history)
    return output