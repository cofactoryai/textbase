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
            from_='YOUR_MOBILE_NUMBER'
        )
        return call.sid
    except Exception as e:
        print(f"Error making the call: {str(e)}")
        return None
    
def suggest_medicine(medicine_name):
    # print(medicine_name)
    api_url = "http://localhost:3000/medicine"
    message = "I am redirecting you to the medicine ordering page where you can easily place your medicine order."
    webbrowser.open(api_url)
    return message

def analyze_user_message(user_message):
    # print(user_message)
    # Use the OpenAI model to analyze the user's message
    ai_response = OpenAI.generate(
        system_prompt = f"Analyze the user message: '{user_message}' and predict the action. If the message contains 'call,' identify the contact name or number, and set the action to 'call.' If the message contains 'order medicine or book medicine or help in booking medicine,' set the action to 'medicine' and recognize the medicine name. If neither 'call' nor 'medicine' is mentioned, set the action to 'unknown.' Provide only relevant words, such as 'call' with a contact or 'medicine' with a medicine's name. Avoid extraneous information. Example1: 'medicine: paracetamal, Tarmazac.' Example2: 'call, 0123456789.' Example3: 'call: Ak.' Please follow the given format examples and do not include other content.",
        message_history=[],
        model="gpt-3.5-turbo",
    )
    # print(type(ai_response))
    # print(ai_response)
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
    user_message = "" 
    response_messages = []
    # print(state)
    user_message = message_history[-1]['content'][0]['value']
    # print(user_message)
        
    action, parameter = analyze_user_message(user_message)
    # print(action)
    # print(parameter)
    state = {'Action':action, 'Parameter':parameter}
    if action == "call":
        call_sid = make_call(parameter)
        if call_sid:
            response_messages.append({
                "data_type": "STRING",
                "value": f"Calling {parameter}... Call ID: {call_sid}"
            })
    
    elif action == "medicine":
        suggested_message = suggest_medicine(parameter)
        response_messages.append({
            "data_type": "STRING",
            "value": suggested_message
        })

    elif action == "unknown":
        # If no specific request, continue with the GPT-3.5 Turbo response
        bot_response = OpenAI.generate(
            system_prompt=SYSTEM_PROMPT,
            message_history=message_history,
            model="gpt-3.5-turbo",
        )

        response_messages.append({
            "data_type": "STRING",
            "value": bot_response
        })

    return {
        "status_code": 200,
        "response": {
            "data": {
                "messages": response_messages,
                "state": state
            },
            "errors": []
        }
    }
