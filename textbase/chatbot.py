# chatbot.py

from .gpt import GPT3Chatbot
from .prompt import PROMPT
from . import registered_chatbots, register

class Chatbot:
    def __init__(self, name):
        """
        The function initializes an object with a given name and creates an instance of the GPT3Chatbot
        class.
        
        :param name: The name parameter is used to initialize the name attribute of the class. It is
        passed as an argument when creating an instance of the class
        """
        self.name = name
        self.gpt_chatbot = GPT3Chatbot()  # Create an instance of GPT3Chatbot

    def process_message(self, message):
        """
        The function takes a user message, generates a response using a GPT chatbot, selects the best
        response, and returns it.
        
        :param message: The `message` parameter in the `process_message` function represents the user's
        input or message that is passed to the chatbot. It is a string that contains the text of the
        user's message
        :return: a string that includes the chatbot's response. The string is formatted as "Chatbot: "
        followed by the bot's response.
        """
        full_prompt = PROMPT + "\nUser: " + message + "\n"
        responses = self.gpt_chatbot.generate_gpt_response(full_prompt)
        bot_response = self.select_best_response(responses)
        return "Chatbot: " + bot_response

    def select_best_response(self, responses):
        return responses[0]

# Register the chatbot class with a name
@register('cologne-chatbot')
class TestChatbot(Chatbot):
    pass
