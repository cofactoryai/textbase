from textbase import bot, Message
from textbase.models import OpenAI
from typing import List
import datetime
import os.path
import pygame
import http.client
from gtts import gTTS
from io import BytesIO
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json
# Load your OpenAI API key
OpenAI.api_key = "YOUR_OPENAI_API_KEY"
Weather_Api_key="YOUR_WEATHERAPI.COM_API_KEY"

# Prompt for GPT-3.5 Turbo
SYSTEM_PROMPT = """You are chatting with an AI. There are no specific prefixes for responses, so you can ask or talk about anything you like.
The AI will respond in a natural, conversational manner. Feel free to start the conversation with any question or topic, and let's have a
pleasant chat!
"""

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

pygame.mixer.init()
def get_weather_details(location):
    host = "api.weatherapi.com"
    endpoint = "/v1/current.json"
    Weather_Api_key = "158941ce62e0452aa31171737230408"
    query_params = f"?key={Weather_Api_key}&q={location}"
    
    conn = http.client.HTTPSConnection(host)
    conn.request("GET", endpoint + query_params)
    response = conn.getresponse()
    data = response.read()
    weather_data = json.loads(data.decode("utf-8"))
    temperature_celsius = weather_data["current"]["temp_c"]
    cloud_coverage = weather_data["current"]["cloud"]
    return temperature_celsius+cloud_coverage

def text_to_speech(text):
    tts = gTTS(text)
    audio_stream = BytesIO()
    tts.save(audio_stream)
    audio_stream.seek(0)
    pygame.mixer.music.load(audio_stream)
    pygame.mixer.music.play()

def get_calendar_events():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'examples/openai-bot/auth.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        events_result = service.events().list(
            calendarId='primary', timeMin=now,
            maxResults=10, singleEvents=True,
            orderBy='startTime').execute()
        events = events_result.get('items', [])
        return events

    except HttpError as error:
        print('An error occurred: %s' % error)



@bot()
def on_message(message_history: List[Message], state: dict = None):
    value = ' '.join(item['content'][0]['value'] for item in message_history) 
    if "show me my events" in value or "display my schedules" in value:
        events = get_calendar_events()

        if events:
            bot_response="Upcoming events:"
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                summary = event['summary']
                bot_response = OpenAI.generate(
                system_prompt=SYSTEM_PROMPT,
                message_history=f'{start} - {summary}',
                model="gpt-3.5-turbo",
                )
            text_to_speech(bot_response)
            return
        else:
            for item in message_history:
                if 'value' in item.get('content', [])[0]:
                    item['content'][0]['value'] = 'No upcoming events'
            bot_response = OpenAI.generate(
            system_prompt=SYSTEM_PROMPT,
            message_history=message_history, 
            model="gpt-3.5-turbo",
            )
    if "weather" in value or "temperature" in value:
        parts = value.split("of")
        if len(parts) > 1:
            city = parts[1].strip()
        temperature=get_weather_details(city)
        for item in message_history:
                if 'value' in item.get('content', [])[0]:
                    item['content'][0]['value'] = city+str(temperature)+"Fahrenhit"
        bot_response = list[message_history]
        formatted_response = {"content": bot_response}
        return
        

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