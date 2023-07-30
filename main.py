import textbase
from textbase.message import Message
from textbase import models
import os
from typing import List
import json 
# Load your OpenAI API key
models.OpenAI.api_key = "key"
# or from environment variable:
# models.OpenAI.api_key = os.getenv("OPENAI_API_KEY")

# Prompt for GPT-3.5 Turbo
SYSTEM_PROMPT = """You are a traffic operator responsible for ensuring safe and efficient traffic flow at intersections. 
You are stationed at the ends of the roads to interact with pedestrians. 
Your role is to respond to their queries, address their concerns, and operate the traffic lights accordingly. 
You have access to the current state of the traffic light, and your responses should ALWAYS be in the following JSON format:

{
  "message": "",
  "state": {
    "possibleState": {
      "red": "stop running vehicles",
      "yellow": "intimation for vehicles to be cautious",
      "green": "vehicles can go ahead freely"
    },
    "selectedState": <the state from the above that you feel should take the next system state of the traffic lights>
  }
}

Please prioritize pedestrian safety and ensure the smooth flow of traffic. Gradually turn the traffic light to red if it's not already in the red state. Also, turn the lights back to green when pedestrians on the other end mention that they have crossed the road. Feel free to respond to pedestrian queries and take appropriate actions to maintain traffic order.
Now, let's proceed with your queries or actions as the traffic operator. Remember to provide responses in the specified JSON format."
Make sure the response is always in the above JSON format strictly.
"""


@textbase.chatbot("talking-bot")
def on_message(message_history: List[Message], state: dict = None):
    """Your chatbot logic here
    message_history: List of user messages
    state: A dictionary to store any stateful information

    Return a string with the bot_response or a tuple of (bot_response: str, new_state: dict)
    """

    # # Generate GPT-3.5 Turbo response
    bot_response = models.OpenAI.generate(
        system_prompt=SYSTEM_PROMPT,
        message_history=message_history,
        model="gpt-3.5-turbo",
    )
    print(bot_response)
    try:
        data = json.loads(bot_response)
    except:
        data = {
            "message": bot_response,
            "state": state
        }
    bot_response, state = data.values()
    return bot_response, state
