import json
import requests
import time
import typing

from textbase.message import Message

class HuggingFace:
    api_key = "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";

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
                "inputs": inputs,
                "max_length": max_tokens,
                "temperature": temperature,
                "min_length": min_tokens,
                "top_k": top_k,
            }
            data = json.dumps(payload)
            response = requests.post(API_URL, headers=headers, json=payload)
            response_data = response.json()

            if response_data.get("error", None) == "Authorization header is invalid, use 'Bearer API_TOKEN'":
                print("Hugging Face API key is not correct")

            if response_data.get("estimated_time", None):
                print(f"Model is loading, please wait for {response_data.get('estimated_time')} seconds")
                time.sleep(response_data.get("estimated_time"))
                response = requests.post(API_URL, headers=headers, json=payload)
                response_data = response.json()

            return response_data["generated_text"]
        except Exception as ex:
            print(f"Error occurred while using this model. Please try using another model. Exception: {ex}")
