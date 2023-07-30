from textbase.message import Message

def test_message_creation():
    content = "Hello, this is a test message."
    role = "user"
    message = Message(content=content, role=role)

    assert message.content == content
    assert message.role == role
