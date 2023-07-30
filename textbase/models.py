import json
import openai
import requests
import typing

from textbase.message import Message


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
        assert cls.api_key is not None, "OpenAI API key is not set"
        openai.api_key = cls.api_key
        print(message_history)
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


class HuggingFace:
    api_key = None

    @classmethod
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
        response = requests.request("POST", API_URL, headers=headers, data=data)
        response = json.loads(response.content.decode("utf-8"))

        return response["generated_text"]