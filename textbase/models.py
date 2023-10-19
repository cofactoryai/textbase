import json
import openai
from io import BytesIO
import google.generativeai as palm
import requests
import time
import typing
import traceback

from textbase import Message


def shorten_url(url):

    static_url = "https://url-shortener-service.p.rapidapi.com/shorten"

    payload = { "url": url }
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "X-RapidAPI-Key": "76049f41a5mshe6af00efc4ac0efp1904efjsn96086296a83b",
        "X-RapidAPI-Host": "url-shortener-service.p.rapidapi.com"
    }

    response = requests.post(static_url, data=payload, headers=headers)

    print(response.json())
    
    return response.json()


# Return list of values of content.
def get_contents(message: Message, data_type: str):
    return [
        {
            "role": message["role"],
            "content": content["value"]
        }
        for content in message["content"]
        if content["data_type"] == data_type
    ]

# Returns content if it's non empty.
def extract_content_values(message: Message, data_type: str="STRING"):
    return [
            content["content"]
            for content in get_contents(message, data_type)
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
        functions=None,
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
            functions=functions,
            function_call="auto",
            temperature=temperature,
            max_tokens=max_tokens,
        )

        res = response["choices"][0]["message"]

        if res.get("function_call"):
            available_functions = {
            "shorten_url": shorten_url,
            
        }
            function_name = res["function_call"]["name"]
            fuction_to_call = available_functions[function_name]
            function_args = json.loads(res["function_call"]["arguments"])
            function_response = fuction_to_call(
            url=function_args.get("url"),
        )
            return function_response['result_url']

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

class PalmAI:
    api_key = None

    @classmethod
    def generate(
        cls,
        message_history: list[Message],
    ):
        assert cls.api_key is not None, "Palm API key is not set."
        palm.configure(api_key=cls.api_key)

        filtered_messages = []

        for message in message_history:
            #list of all the contents inside a single message
            contents = extract_content_values(message)
            if contents:
                filtered_messages.extend(contents)

        #send request to Google Palm chat API
        response = palm.chat(messages=filtered_messages)

        print(response)
        return response.last

class DallE:
    api_key = None

    @classmethod
    def generate(
        cls,
        message_history: list[Message],
        size="256x256"
    ):
        assert cls.api_key is not None, "OpenAI API key is not set."
        openai.api_key = cls.api_key

        last_message = message_history[-1]
        prompt = extract_content_values(last_message)[0]

        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size=size,
        )
        return response['data'][0]['url']

    @classmethod
    def generate_variations(
        cls,
        message_history: list[Message],
        size="256x256"
    ):
        assert cls.api_key is not None, "OpenAI API key is not set."
        openai.api_key = cls.api_key

        last_message = message_history[-1]
        image_url = extract_content_values(last_message, "IMAGE_URL")[0]

        response = requests.get(image_url)
        image_content = BytesIO(response.content)

        response = openai.Image.create_variation(
            image=image_content,
            n=1,
            size=size,
        )

        return response['data'][0]['url']
