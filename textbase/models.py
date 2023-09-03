import json
import openai
import requests
import time
import typing
import traceback
import cohere

from textbase import Message

# Return list of values of content.
def get_contents(message: Message, data_type: str, client: str = None):
    return [
        {
            "user_name": message["role"],
            "message": content["value"]
        }
        if content["data_type"] == data_type and client == "cohere"
        else 
        {
            "role": message["role"],
            "content": content["value"]
        }
        if content["data_type"] == data_type
        else
        f"Content data type is not {data_type}"
        for content in message["content"]
    ]

# Returns content if it's non empty.
def extract_content_values(message: Message):
    return [
            content["content"]
            for content in get_contents(message, "STRING")
            if content
        ]

class OpenAI:
    api_key = None

    @classmethod
    def generate(
        cls,
        system_prompt: str,
        message_history: list[Message],
        model="gpt-3.5-turbo",
        max_tokens=3000,
        temperature=0.7,
    ):
        assert cls.api_key is not None, "OpenAI API key is not set."
        openai.api_key = cls.api_key

        filtered_messages = []

        for message in message_history:
            #list of all the contents inside a single message
            contents = get_contents(message, "STRING")
            if contents:
                filtered_messages.extend(contents)

        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                *map(dict, filtered_messages),
            ],
            temperature=temperature,
            max_tokens=max_tokens,
        )

        return response["choices"][0]["message"]["content"]

class HuggingFace:
    api_key = None

    @classmethod
    def generate(
        cls,
        system_prompt: str,
        message_history: list[Message],
        model: typing.Optional[str] = "microsoft/DialoGPT-large",
        max_tokens: typing.Optional[int] = 3000,
        temperature: typing.Optional[float] = 0.7,
        min_tokens: typing.Optional[int] = None,
        top_k: typing.Optional[int] = None
    ) -> str:
        try:
            assert cls.api_key is not None, "Hugging Face API key is not set."

            headers = { "Authorization": f"Bearer { cls.api_key }" }
            API_URL = "https://api-inference.huggingface.co/models/" + model
            inputs = {
                "past_user_inputs": [system_prompt],
                "generated_responses": [f"Ok, I will answer according to the context, where context is '{system_prompt}'."],
                "text": ""
            }

            for message in message_history:
                if message["role"] == "user":
                    inputs["past_user_inputs"].extend(extract_content_values(message))
                else:
                    inputs["generated_responses"].extend(extract_content_values(message))

            inputs["text"] = inputs["past_user_inputs"].pop(-1)

            payload = {
                "inputs": inputs,
                "max_length": max_tokens,
                "temperature": temperature,
                "min_length": min_tokens,
                "top_k": top_k,
            }

            data = json.dumps(payload)
            response = requests.request("POST", API_URL, headers=headers, data=data)
            response = json.loads(response.content.decode("utf-8"))

            if response.get("error", None) == "Authorization header is invalid, use 'Bearer API_TOKEN'.":
                print("Hugging Face API key is not correct.")

            if response.get("estimated_time", None):
                print(f"Model is loading please wait for {response.get('estimated_time')}")
                time.sleep(response.get("estimated_time"))
                response = requests.request("POST", API_URL, headers=headers, data=data)
                response = json.loads(response.content.decode("utf-8"))

            return response["generated_text"]

        except Exception:
            print(f"An exception occured while using this model, please try using another model.\nException: {traceback.format_exc()}.")

class BotLibre:
    application = None
    instance = None

    @classmethod
    def generate(
        cls,
        message_history: list[Message],
    ):
        most_recent_message = get_contents(message_history[-1], "STRING")

        request = {
            "application": cls.application,
            "instance": cls.instance,
            "message": most_recent_message
        }
        response = requests.post('https://www.botlibre.com/rest/json/chat', json=request)
        data = json.loads(response.text) # parse the JSON data into a dictionary
        message = data['message']

        return message
    

class Cohere:
    api_key = None

    @classmethod
    def generate(
        cls,
        system_prompt: str,
        message_history: list[Message],
        model: str = "command",
        max_tokens=3500,
        temperature=0.5,
    ):
        assert cls.api_key is not None, "Cohere API key is not set."
        filtered_messages = []

        for message in message_history:
            #list of all the contents inside a single message
            contents = get_contents(message, "STRING")
            if contents:
                filtered_messages.extend(contents)
        cohere_client = cohere.Client(cls.api_key)
        response = cohere_client.generate(
            prompt=system_prompt,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response[0]
    
    @classmethod
    def chat(
        cls,
        system_prompt: str,
        user_name:str,
        message_history: list[Message],
        model: str = "command",
        max_tokens=1500,
        temperature=0.5,
    ):
        
        """
        Engage in a chat conversation using the Cohere API.

        Args:
            cls (object): The class object containing the Cohere API key.
            system_prompt (str): The initial system prompt or message to start the conversation.
            user_name (str): The user's name or identifier in the conversation.
            message_history (list[Message]): A list of messages representing the chat history.
            model (str, optional): The model to use for the chat conversation. Defaults to "command".
            max_tokens (int, optional): The maximum number of tokens in the generated response. Defaults to 1500.
            temperature (float, optional): The temperature parameter for generating responses. 
                Higher values (e.g., 1.0) make the output more random, while lower values (e.g., 0.1) make it more deterministic. Defaults to 0.5.

        Returns:
            str: The text of the response generated by the Cohere API as part of the chat conversation.

        Raises:
            AssertionError: Raised when the Cohere API key is not set.

        Example:
            To have a chat conversation using the Cohere API:
            ```
            api_key = "your_api_key_here"
            system_prompt = "System: Welcome to the chatbot. How can I assist you today?"
            user_name = "User123"
            message_history = []  # You can add previous messages to the history
            result = chat(api_key, system_prompt, user_name, message_history)
            print(result)
            ```
        """
        assert cls.api_key is not None, "Cohere API key is not set."
        filtered_messages = []

        for message in message_history:
            #list of all the contents inside a single message
            contents = get_contents(message, "STRING","cohere")
            if contents:
                filtered_messages.extend(contents)
        
        # initializing cohere client
        cohere_client = cohere.Client(cls.api_key)
        
        response = cohere_client.chat(
            message=system_prompt,
            user_name=user_name,
            model=model,
            chat_history=[
                {
                    "user_name": "system",
                    "message": system_prompt
                },
                *map(dict, filtered_messages),
            ],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        
        return response.text
    
    @classmethod
    def summarize(
        cls,
        text_input: str,
        message_history: list[Message],
        model: str = "command",
        temperature=0.3,
        length:str = "medium",
        format:str = "paragraph",
    ):
        """
        Summarize a text_input using the Cohere API based on a text input.

        Args:
            cls (object): The class object containing the Cohere API key.
            text_input (str): The input text to be summarized.
            message_history (list[Message]): A list of messages to consider in the summarization process.
            model (str, optional): The model to use for summarization. Defaults to "command".
            temperature (float, optional): The temperature parameter for generating the summary. 
                Higher values (e.g., 1.0) make the output more random, while lower values (e.g., 0.1) make it more deterministic. Defaults to 0.3.
            length (str, optional): The desired length of the summary. 
                Options include "short," "medium," and "long." Defaults to "medium".
            format (str, optional): The desired format of the summary, e.g., "paragraph" or other formats supported by Cohere. Defaults to "paragraph".

        Returns:
            str: The summarized text generated by the Cohere API.

        Raises:
            AssertionError: Raised when the Cohere API key is not set.

        Example:
            To summarize a text with a text input using the default parameters:
            ```
            api_key = "your_api_key_here"
            result = summarize(api_key, "This is the input text.", message_history)
            print(result)
            ```
        """
        assert cls.api_key is not None, "Cohere API key is not set."
        filtered_messages = []

        for message in message_history:
            #list of all the contents inside a single message
            contents = get_contents(message, "STRING")
            if contents:
                filtered_messages.extend(contents)
        
        # initializing cohere client
        cohere_client = cohere.Client(cls.api_key)
        
        response =cohere_client.summarize(
            text=text_input,
            length=length,
            format=format,
            model=model,
            temperature=temperature,
        )
        
        return response.summary
    