from textbase import bot, Message
from textbase.models import Cohere
from typing import List

# Load your Cohere API key
Cohere.api_key = ""

# Prompt for `command` (cohere's model)
# you add your sample prompts here
SYSTEM_PROMPT = """"Ice cream is a sweetened frozen food typically eaten as a snack or dessert. 
  It may be made from milk or cream and is flavoured with a sweetener, 
  either sugar or an alternative, and a spice, such as cocoa or vanilla, 
  or with fruit such as strawberries or peaches. 
  It can also be made by whisking a flavored cream base and liquid nitrogen together. 
  Food coloring is sometimes added, in addition to stabilizers. 
  The mixture is cooled below the freezing point of water and stirred to incorporate air spaces 
  and to prevent detectable ice crystals from forming. The result is a smooth, 
  semi-solid foam that is solid at very low temperatures (below 2 °C or 35 °F). 
  It becomes more malleable as its temperature increases.
  The meaning of the name ice cream varies from one country to another. 
  In some countries, such as the United States, ice cream applies only to a specific variety, 
  and most governments regulate the commercial use of the various terms according to the 
  relative quantities of the main ingredients, notably the amount of cream. 
  Products that do not meet the criteria to be called ice cream are sometimes labelled 
  frozen dairy dessert instead. In other countries, such as Italy and Argentina, 
  one word is used for all variants. Analogues made from dairy alternatives, 
  such as goat's or sheep's milk, or milk substitutes 
  (e.g., soy, cashew, coconut, almond milk or tofu), are available for those who are 
  lactose intolerant, allergic to dairy protein or vegan.
"""

@bot()
def on_message(message_history: List[Message], state: dict = None):

    # Generate `command` (cohere's model) response
    bot_response = Cohere.summarize(
        text_input=SYSTEM_PROMPT,
        message_history=message_history, # Assuming history is the list of user messages
        model="command",
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