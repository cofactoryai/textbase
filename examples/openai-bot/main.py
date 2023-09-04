from textbase import bot, Message
from textbase.models import OpenAI
from typing import List
import requests
import webbrowser
from twilio.rest import Client
import re

account_sid = 'ENTER_YOUR_TWILIO_SID'
auth_token = 'ENTER_YOUR_TWILIO_TOKEN'
client = Client(account_sid, auth_token)
# Load your OpenAI API key
OpenAI.api_key = "ENTER_YOUR_OPENAI_API_KEY"

# Prompt for GPT-3.5 Turbo
SYSTEM_PROMPT = """
    "You are trusted HealthBuddy, you want to help people by replying to message above 98 words with bulllet points all messages like How can I..., Call Mom..., Suggest Medicine... in this prompt and responding accordingly.",
    "How can I assist you with your health today? Feel free to ask any health-related questions or make requests like:",
    "- Call Mom/Dad/Emergency/<given number>",
    "- Suggest medicine and order it",
    "- General Health Inquiry",
    "- Symptom Checker",
    "- Medication Reminders",
    "- Health Tips",
    "- Medical Conditions Information",
    "- Mental Health Support",
    "- COVID-19 Information",
    "- Healthy Lifestyle Tips",
    "Simply choose from the options above, or type your question or request, and let's get started on your path to better health!"
"""

def make_call(contact):
    try:
        # Create a call
        call = client.calls.create(
            twiml=f'<Response><Say>Calling {contact}...</Say></Response>',
            to=f'+91{contact}',
            from_='+16562185538'
        )
        return call.sid
    except Exception as e:
        print(f"Error making the call: {str(e)}")
        return None
    
def suggest_medicine(medicine_name):
    print(medicine_name)
    api_url = "http://localhost:3000/medicine"
    webbrowser.open(api_url)
    message = "I am redirecting you to the medicine ordering page where you can easily place your medicine order."
    return message

def analyze_user_message(user_message):
    print(user_message)
    # Use the OpenAI model to analyze the user's message
    ai_response = OpenAI.generate(
        system_prompt = f"Analyze the user message: '{user_message}' and predict the action if message content call or medicine keyword otherwise return unknown. If the user wants to make a phone call, identify the contact name or number. If the user wants to order medicine, recognize the medicine name. Provide only relevant words, such as 'call' with a contact or 'medicine' with a medicines name. Avoid extraneous information. exmaple1: medicine: paracetamal, Tarmazac. example2: call, 0123456789. example3: call: Ak. Give only given format exmples and do not write other way and other content.",
        message_history=[],
        model="gpt-3.5-turbo",
    )
    print(type(ai_response))
    print(ai_response)
    # i want to orderd medicine please help mu to buy Tramazac , paracetamal, suncold
    keywords = re.findall(r'\b(call|medicine|\w+|\d+)\b', ai_response.lower())
    action = None
    contact = None
    medicine = None
    
    # Process the found keywords
    for i in range(len(keywords)):
        if keywords[i] == "call":
            action = "call"
            for j in range(i + 1, len(keywords)):
                if keywords[j].isdigit() or keywords[j].isalpha():
                    contact = keywords[j]
                    return action, contact
        elif keywords[i] == "medicine":
            action = "medicine"
            for j in range(i + 1, len(keywords)):
                if keywords[j].isalpha():
                    medicine = keywords[j]
                    return action, medicine
    
    return "unknown", None


@bot()
def on_message(message_history: List[Message], state: dict = None):
    if message_history:
        user_message = message_history[0]['content'][0]['value']
        action, parameter = analyze_user_message(user_message)
        print(action)
        print(parameter)
        if action == "call":
            call_sid = make_call(parameter)
            if call_sid:
                return {
                    "status_code": 200,
                    "response": {
                        "data": {
                            "messages": [
                                {
                                    "data_type": "STRING",
                                    "value": f"Calling {parameter}... Call ID: {call_sid}"
                                }
                            ],
                            "state": state
                        },
                        "errors": []
                    }
                }
        elif action == "medicine":
            suggested_messaage = suggest_medicine(parameter)
            return {
                "status_code": 200,
                "response": {
                    "data": {
                        "messages": [
                            {
                                "data_type": "STRING",
                                "value": suggested_messaage
                            }
                        ],
                        "state": state
                    },
                    "errors": []
                }
            }
        elif action == "unknown":
            # If no specific request, continue with the GPT-3.5 Turbo response
            bot_response = OpenAI.generate(
                system_prompt=SYSTEM_PROMPT,
                message_history=message_history,
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