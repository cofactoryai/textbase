# textbase/message.py
from pydantic import BaseModel


class Message(BaseModel):
    content: str
    role: str  # "user" or "assistant"


    def __hash__(self):
        # Hash based on the combination of content and role
        hashed_value = hash((self.content, self.role))
        return hashed_value

    def __eq__(self, other):
        # Compare content and role for equality
        if not isinstance(other, Message):
            return False
        return self.content == other.content and self.role == other.role