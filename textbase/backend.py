# textbase/backend.py
from fastapi import FastAPI
from fastapi import File, UploadFile
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
import shutil
from textbase.document_search import DocumentChat

logging.basicConfig(level=logging.INFO)

load_dotenv()

from .message import Message

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
    """
    The `read_root` function reads and returns the contents of an HTML file specified by the path
    "textbase/frontend/index.html".
    :return: The content of the "index.html" file located in the "textbase/frontend" directory is being
    returned.
    """
    with open("textbase/frontend/dist/index.html") as f:
        try:
            os.remove("textbase/dump/context.bin")
        except:
            pass
        return f.read()
    


def get_module_from_file_path(file_path: str):
    """
    The function `get_module_from_file_path` takes a file path as input, loads the module from the file,
    and returns the module.

    :param file_path: The file path is the path to the Python file that you want to import as a module.
    It should be a string representing the absolute or relative path to the file
    :type file_path: str
    :return: the module that is loaded from the given file path.
    """
    module_name = os.path.splitext(os.path.basename(file_path))[0]
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

        
@app.post("/upload")
def upload(file: UploadFile = File(...)):
    try:
        os.makedirs('textbase/dump/',exist_ok=True)
        with open('textbase/dump/context.bin', 'wb') as f:
            shutil.copyfileobj(file.file, f)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()
        
    return {"message": f"Successfully uploaded context.bin"}



@app.post("/chat", response_model=dict)
async def chat(messages: List[Message], state: dict = None):
    """
    The above function is a Python API endpoint that receives a list of messages and a state dictionary,
    loads a module from a file path, calls the on_message function from the module with the messages and
    state, and returns the bot messages generated by the module.

    :param messages: The `messages` parameter is a list of `Message` objects. It represents the messages
    exchanged between the user and the chatbot. Each `Message` object typically contains information
    such as the text of the message, the sender, the timestamp, etc
    :type messages: List[Message]
    :param state: The `state` parameter is a dictionary that stores the state of the conversation. It
    can be used to store information or context that needs to be maintained across multiple requests or
    messages in the conversation. The `state` parameter is optional and can be set to `None` if not
    needed
    :type state: dict
    :return: a list of `Message` objects.
    """

    ## check whether context is available 
    context_path = 'textbase/dump/context.bin'
    bin_file,ask_from_doc = None,None
    if os.path.exists(context_path):
        bin_file = open(context_path,'rb')
        ask_from_doc = DocumentChat(bin_file)
        print('context exists!')


    file_path = os.environ.get("FILE_PATH", None)
    logging.info(file_path)
    if not file_path:
        return []

    module = get_module_from_file_path(file_path)

    print("here", state)

    # Call the on_message function from the dynamically loaded module
    if ask_from_doc:
        query = messages[-1].content
        chunks = ask_from_doc.search_for_query(query)
        print(query, chunks)
        SYSTEM_PROMPT = ask_from_doc.SYSTEM_PROMPT(chunks)

        response = module.on_message(messages, state , SYSTEM_PROMPT = SYSTEM_PROMPT)
    else:
        response = module.on_message(messages, state)
    print(response)
    if type(response) is tuple:
        bot_response, new_state = response
        return {
            "botResponse": {"content": bot_response, "role": "assistant"},
            "newState": new_state,
        }
    elif type(response) is str:
        return {"botResponse": {"content": response, "role": "assistant"}}


# Mount the static directory (frontend files)
app.mount(
    "/assets",
    StaticFiles(directory="textbase/frontend/dist/assets", html=True),
    name="static",
)
