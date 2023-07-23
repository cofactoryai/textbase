# textbase/backend.py
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles  
from fastapi.responses import HTMLResponse
from textbase.message import Message
from dotenv import load_dotenv
import os
import sys
from typing import List

load_dotenv()

from .message import Message  

# Get the path of the directory containing this file (backend.py)
current_dir = os.path.dirname(os.path.abspath(__file__))
# Add the parent directory of backend.py to the Python path
parent_dir = os.path.join(current_dir, "..")
sys.path.append(parent_dir)
from main import on_message


app = FastAPI()
app.mount("/static", StaticFiles(directory="textbase/frontend/public"), name="static")  # Mount the static directory
templates = Jinja2Templates(directory="textbase/frontend/templates")  # Directory path for templates

@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})

@app.post('/chat', response_model=List[Message])
async def chat(messages: List[Message], state: dict = None):
    
    # Call the on_message function from main module to get chatbot's response
    bot_messages, new_state = on_message(messages, state)

    return bot_messages
