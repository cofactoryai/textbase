from typing import List
from textbase import bot, Message
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
import os

# added claude from antropic 


anthropic = Anthropic(
    api_key= os.environ["ANTHROPIC_API_KEY"],
)

   
SYSTEM_PROMPT=f"{HUMAN_PROMPT} I am a general purpose Generative AI how can I help you?{AI_PROMPT}"


@bot()
def on_message(message_history: List[Message], state: dict = None):

    completion = anthropic.completions.create(
        message_history=message_history, # Assuming history is the list of user messages
         model="claude-2",
    max_tokens_to_sample=300,
    prompt = SYSTEM_PROMPT
    )

    return {
        "messages": [completion.completion],
        "state": state
    }
