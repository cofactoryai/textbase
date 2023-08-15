from fastapi import FastAPI
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

logging.basicConfig(level=logging.INFO)

load_dotenv()

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:4000",
    "http://localhost:5173",
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("textbase/frontend/dist/index.html") as f:
        return f.read()

def get_module_from_file_path(file_path: str):
    module_name = os.path.splitext(os.path.basename(file_path))[0]
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

# Set the FILE_PATH environment variable to the location of your chatbot logic module
os.environ["FILE_PATH"] = "textbase\examples\huggingface\main.py"

@app.post("/chat", response_model=dict)
async def chat(messages: List[Message], state: dict = None):
    file_path = os.environ.get("FILE_PATH", None)
    logging.info(file_path)
    if not file_path:
        return []

    module = get_module_from_file_path(file_path)

    response = module.on_message(messages, state)
    if type(response) is tuple:
        bot_response, new_state = response
        return {
            "botResponse": {"content": bot_response, "role": "assistant"},
            "newState": new_state,
        }
    elif type(response) is str:
        return {"botResponse": {"content": response, "role": "assistant"}}

app.mount(
    "/assets",
    StaticFiles(directory="textbase/frontend/dist/assets", html=True),
    name="static",
)
