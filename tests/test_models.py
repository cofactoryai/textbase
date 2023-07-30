from textbase.models import OpenAI
import pytest


def test_generate_with_valid_api_key():
    OpenAI.api_key = "valid_api_key"
    # Your test logic here, for example:
    response = OpenAI.generate("Test system prompt", [])
    assert response is not None

def test_generate_with_invalid_api_key():
    OpenAI.api_key = "invalid_api_key"
    with pytest.raises(AssertionError):
        OpenAI.generate("Test system prompt", [])

