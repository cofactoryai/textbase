---
sidebar_position: 4
---

# WhatsAppSMS - AI Pizza Order Bot

This is AI pizza order bot that uses Whatsapp message API to send order details to the user. It uses the [Twilio API](https://www.twilio.com/whatsapp) to send messages to the user.

AI pizza order bot example is used to showcase the usecase of this Messaging Service. 

Do check `textbase/whatsappmsg.py` from project file for more details on the Twilio methods used here to send messages.

```py
import os
from textbase import bot, Message
from textbase.models import OpenAI
from textbase.models import HuggingFace as Hu
from typing import List
from textbase import whatsappmsg as sms

# Load your OpenAI API key & twilio required tokens & sid 
# OpenAI.api_key = ""
# or from environment variable:
OpenAI.api_key = os.getenv("OPENAI_API_KEY")
sms.Twilio.account_sid = os.getenv("TWILIO_ACCOUNT_SID")
sms.Twilio.auth_token = os.getenv("TWILIO_AUTH_TOKEN")
sms.Twilio.msgServiceSid = os.getenv("TWILIO_MSG_SERVICE_SID")
sms.Twilio.phonenumber = os.getenv("TWILIO_FROM_NUMBER")

# Prompt for GPT-3.5 Turbo
SYSTEM_PROMPT = """
You are AI assistant service to collect orders for textbase pizza restaurant. \
You respond in a short, very conversational friendly style. \
Adress = textbase pizza , 1st floor ,City Mall \
1. You first greet the customer, ask for their user to make it personalized,\
2. Collects the order from the menu given below step by step
[important]Make sure to clarify all options,sizes, toppings to uniquely \ Remeber asking about Drinks as\
identify the items from the menu.\
You wait to collect the entire order, then summarize including price it and check for a final \
time if the customer wants to add anything else. \
3. then asks if it's a pickup or delivery. \
If it's a delivery, you ask for an address. \
4. then ask user's phone numbe.r \
5. Finally you collect the payment.\ 
7.[important]At last start with "Thank you for placing your order " and add [ 4digit real order number , total summary of order
 -all components,  total price, address, aprx time , phone number ]  with a better presentation
Menu - pizzas, toppings, & drinks\
Pizzas:
- Pepperoni Pizza: ₹300, ₹450, ₹600
- Cheese Pizza: ₹250, ₹400, ₹550
- Farmhouse Pizza: ₹280, ₹420, ₹580
- Paneer Tikka Pizza: ₹320, ₹480, ₹640
- Butter Chicken Pizza: ₹340, ₹500, ₹670
- Tandoori Veggie Pizza: ₹300, ₹460, ₹620
- Masala Fries: ₹120, ₹180
- Paneer Tikka Salad: ₹200
Toppings: 
- Extra Paneer: ₹40
- Sliced Bell Peppers: ₹20
- Sliced Red Onions: ₹15
- Sliced Tomatoes: ₹15
- Fresh Coriander: ₹10
Drinks:
- Pepsi: ₹40, ₹50, ₹60
- Coke: ₹40, ₹50, ₹60
- Lassi: ₹60, ₹70, ₹80
- Bottled Water: ₹20
"""
# Creating global varibales to store phone number out of bot response to send order details later 
phone_number = None
# Condtion to check if the bot send bot response to whatsapp based on you bot response on customized prompt
check_to_send_order_details = "Thank you for placing your order"

@bot()
def on_message(message_history: List[Message], state: dict = None):

    # Genrate OpenAI response. Uses the gpt-3.5-turbpp by default.
    bot_response = OpenAI.generate(
        system_prompt=SYSTEM_PROMPT,
        message_history=message_history, # Assuming history is the list of user messages
    )

    # Whatsapp Messagin service for sending order details
    global phone_number 
    # Checking if the bot response contains phone number
    phone_number = sms.Twilio.extract_phone_number(bot_response)
    if check_to_send_order_details in bot_response:
        #sending the bots order details to the user
        sms.Twilio.sendsms(details=bot_response,send_to=phone_number)

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
```

## How to run this example?

When the user inputs his/her phone number in the chat, the bot will put the phone number in the global variable `phone_number` and then the bot will check the conditon `check_to_send_order_details` & send the order details to the user by calling the `sendsms` method from the `Twilio` class.

Important things to keep in mind while writing System Prompt to implement whatsapp sms:

- For this you have to what to send as the output to the user in the `check_to_send_order_details` variable to match the bot response.

    example: `check_to_send_order_details = "Thank you for placing your order"`

- Don't forget to ask user input of phone number in the bot response.