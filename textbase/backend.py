# textbase/backend.py
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from textbase.message import Message
from dotenv import load_dotenv
import os
from fastapi.middleware.cors import CORSMiddleware
import sys
import logging
from typing import List
import importlib
from pathlib import Path

HOME = Path.home()

logging.basicConfig(level=logging.INFO)

load_dotenv()

from .message import Message

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:4000",
    "http://localhost:5173",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=f"{HOME}/.local/share/textbase_frontend", html=True), name="static")  # Mount the static directory

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open(f"{HOME}/.local/share/textbase_frontend/index.html") as f:
        return f.read()

def get_module_from_file_path(file_path: str):
    module_name = os.path.splitext(os.path.basename(file_path))[0]
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

@app.post("/chat", response_model=List[Message])
async def chat(messages: List[Message], state: dict = None):
    file_path = os.environ.get("FILE_PATH", None)
    logging.info(file_path)
    if not file_path:
        return []

    module = get_module_from_file_path(file_path)

    # Call the on_message function from the dynamically loaded module
    bot_messages, new_state = module.on_message(messages, state)
    return bot_messages
