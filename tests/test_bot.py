from textbase.bot import bot
import unittest
from unittest.mock import Mock
from main import on_message
from flask import Request
from typing import List
from textbase import bot
from textbase.message import Message
from main import on_message

class TestBot(unittest.TestCase):

    def mock_bot_request(self, history_messages, state):
        return {'status_code': 200, 'response': {'data': {'messages': [{'data_type': 'STRING', 'value': 'Hello World'}], 'state': {}}, 'errors': [{'message': ''}]}}
    
    def test_bot(self):
        """
            Test the bot decorator
        """
        # Create a mock request object
        mock_request = Mock(method='GET', json={'data': {'message_history': [], 'state': {}}})
        
        bot_message = bot()
        decorated_mock_func = bot_message(self.mock_bot_request)
        result = decorated_mock_func(mock_request)
        self.assertEqual(result[0]['new_message'], [{'data_type': 'STRING', 'value': 'Hello World'}])
    
    def test_bot_options(self):
        """
            Test the bot decorator with an OPTIONS request
        """
        # Create a mock request object with method set to 'OPTIONS'
        mock_request = Mock(method='OPTIONS', json={'data': {'message_history': [], 'state': {}}})
        
        bot_message = bot()
        
        decorated_mock_func = bot_message(self.mock_bot_request)
        result = decorated_mock_func(mock_request)
        self.assertEqual(result[0], '')
        self.assertEqual(result[1], 204)
        self.assertEqual(result[2], {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        })
    
    def test_bot_non_list_history_messages(self):
        """
            Test the bot decorator with a non-list value for history_messages
        """
        # Create a mock request object with history_messages set to a non-list value
        mock_request = Mock(method='GET', json={'data': {'message_history': 'not a list', 'state': {}}}, spec=Request)
    
        bot_message = bot()
        decorated_mock_func = bot_message(self.mock_bot_request)

        result = decorated_mock_func(mock_request)
        self.assertEqual(result[0], 'Error in processing')
        self.assertEqual(result[1], 402)

    def test_on_message(self):
        mock_request = Mock(spec=Request, method = "POST", json = {"data":{"message_history":[{"role":"user","content":[{"data_type":"STRING","value":"Hello World"}]}],"state":{}}})
        message_history = mock_request
        result = on_message(message_history)

        #Tuple 0th index is reponse
        response_data = result[0]
        assert type(response_data["message_history"]) is list
        assert type(response_data["state"]) is dict

        assert type(response_data["message_history"][0]["role"]) is str
        assert type(response_data["message_history"][0]["content"]) is list
        assert type(response_data["message_history"][0]["content"][0]["data_type"]) is str
        assert type(response_data["message_history"][0]["content"][0]["value"]) is str

        assert type(response_data["new_message"]) is list
        assert type(response_data["new_message"][0]["data_type"]) is str
        assert type(response_data["new_message"][0]["value"]) is str

        # Last Message in message history is the same as New Message
        assert response_data["message_history"][-1]["role"] == "assistant"

        # Tuple 1st index is status code
        assert result[1] == 200

        # Tuple 2nd index is Headers
        assert result[2] == {'Access-Control-Allow-Origin': '*'}
