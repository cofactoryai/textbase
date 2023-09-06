import pytest
from textbase import bot

class MockRequest:
    def __init__(self, method, json_data):
        self.method = method
        self.json_data = json_data

def mock_bot_function(*args):
    request = args[0]
    response = ('', 204, {'Access-Control-Allow-Origin': '*'})
    return response

def test_bot():
    mock_request = MockRequest("OPTIONS", {
        "data": {
            "message_history": [],
            "state": {}
        }
    })
    result = bot()(mock_bot_function)(mock_request)
    assert isinstance(result, tuple)
    assert len(result) == 3
    expected_headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600'
    }
    assert result[2] == expected_headers
    assert result[0] == ''
    assert result[1] == 204

