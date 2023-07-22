# textbase/backend.py
from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles  
from fastapi.responses import HTMLResponse
from textbase.message import Message
from dotenv import load_dotenv
import os

load_dotenv()

import openai  
from typing import List
from .message import Message  
from .prompt import PROMPT  


app = FastAPI()
app.mount("/static", StaticFiles(directory="textbase/frontend/public"), name="static")  # Mount the static directory
templates = Jinja2Templates(directory="textbase/frontend/templates")  # Directory path for templates

@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})

@app.post('/chat', response_model=list[Message])
async def chat(messages: list[Message], state: dict = None):
    # Handle user messages using the user-provided chatbot function
    # You should replace the following function with the user-provided chatbot logic.
    bot_messages = process_messages(messages)

    return bot_messages

def process_messages(messages: List[Message]):
    bot_messages = []
    for message in messages:
        # Prepare the user message as a single string for GPT input
        user_input = f"User: {message.text}"
        full_prompt = f"{PROMPT}\n{user_input}\n"

        # Generate GPT response using your API
        gpt_response = generate_gpt_response(full_prompt)
        bot_response = gpt_response[0] if gpt_response else "ChatGPT: I'm sorry, I couldn't generate a response for that."

        bot_messages.append(Message(text=bot_response, sender='bot'))

    return bot_messages

def generate_gpt_response(prompt: str):
    openai.api_key = os.getenv('OPENAI_API_KEY')  

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  
        messages=[{"role": "system", "content": PROMPT}, {"role": "user", "content": prompt}],
        temperature=0.7,  
        max_tokens=3500,  
        n=1,  
        presence_penalty=0.0,
        frequency_penalty=0.0,  
    )

    generated_texts = [choice["message"]["content"].strip() for choice in response["choices"]]
    return generated_texts