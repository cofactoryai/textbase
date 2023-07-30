# textbase/message.py
from pydantic import BaseModel


class Message(BaseModel):
    content: str
    role: str  # "user" or "assistant"

class FormData(BaseModel):
    selectedOption: str
    selectedSubOption: str
    apiKey: str
