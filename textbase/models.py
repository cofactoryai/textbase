import json
import openai
import requests
import time
import typing
import logging
from functools import lru_cache

from textbase.message import Message

def cached_generate(cls, cache_key, request_function):
    if cache_key in cls.cached_responses:
        return cls.cached_responses[cache_key]

    response = request_function()
    cls.cached_responses[cache_key] = response
    return response

class OpenAI:
    api_key = None
    cached_responses = {}

    @classmethod
    @lru_cache(maxsize=128)
    def generate(
        cls,
        system_prompt: str,
        message_history: list[Message],
        model="gpt-3.5-turbo",
        max_tokens=3000,
        temperature=0.7,
    ):
        assert cls.api_key is not None, "OpenAI API key is not set"
        openai.api_key = cls.api_key

        def request_function():
            response = openai.ChatCompletion.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    *map(dict, message_history),
                ],
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return response["choices"][0]["message"]["content"]

        cache_key = (system_prompt, tuple(message_history))
        return cached_generate(cls, cache_key, request_function)

class HuggingFace:
    api_key = None
    cached_responses = {}

    @classmethod
    @lru_cache(maxsize=128)
    def generate(
        cls,
        system_prompt: str,
        message_history: list[Message],
        model: typing.Optional[str] = "microsoft/DialoGPT-small",
        max_tokens: typing.Optional[int] = 3000,
        temperature: typing.Optional[float] = 0.7,
        min_tokens: typing.Optional[int] = None,
        top_k: typing.Optional[int] = None
    ) -> str:
        try:
            assert cls.api_key is not None, "Hugging Face API key is not set"

            headers = {"Authorization": f"Bearer {cls.api_key}"}
            API_URL = "https://api-inference.huggingface.co/models/" + model
            inputs = {
                "past_user_inputs": [system_prompt],
                "generated_responses": [f"ok I will answer according to the context, where context is '{system_prompt}'"],
                "text": ""
            }

            for message in message_history:
                if message.role == "user":
                    inputs["past_user_inputs"].append(message.content)
                else:
                    inputs["generated_responses"].append(message.content)

            inputs["text"] = inputs["past_user_inputs"].pop(-1)
            payload = {
                "inputs":inputs,
                "max_length": max_tokens,
                "temperature": temperature,
                "min_length": min_tokens,
                "top_k": top_k,
            }
            data = json.dumps(payload)

            def request_function():
                response = requests.request("POST", API_URL, headers=headers, data=data)
                response = json.loads(response.content.decode("utf-8"))
                if response.get("error", None) == "Authorization header is invalid, use 'Bearer API_TOKEN'":
                    error_message = "Hugging Face API key is not correct"
                    logging.error(error_message)

                if response.get("estimated_time", None):
                    estimated_time = response.get("estimated_time")
                    logging.info(f"Model is loading. Please wait for {estimated_time} seconds.")
                    time.sleep(estimated_time)
                    response = requests.request("POST", API_URL, headers=headers, data=data)
                    response = json.loads(response.content.decode("utf-8"))

                return response["generated_text"]

            cache_key = (system_prompt, tuple(message_history))
            return cached_generate(cls, cache_key, request_function)
        except Exception as ex:
            error_message = f"HuggingFace Error: {str(ex)}"
            logging.error(error_message)
            raise

class BotLibre:
    application = None
    instance = None
    cached_responses = {}

    @classmethod
    @lru_cache(maxsize=128)
    def generate(
        cls,
        message_history: list[Message],
    ):
        try:
            request = {"application": cls.application, "instance": cls.instance, "message": message_history[-1].content}

            def request_function():
                response = requests.post('https://www.botlibre.com/rest/json/chat', json=request)
                data = json.loads(response.text)  # parse the JSON data into a dictionary
                message = data['message']
                return message

            cache_key = tuple(message_history)
            return cached_generate(cls, cache_key, request_function)
        except Exception as ex:
            error_message = f"BotLibre Error: {str(ex)}"
            logging.error(error_message)
            raise
