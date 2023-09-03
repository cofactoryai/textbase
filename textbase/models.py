import json
import openai
import google.generativeai as palm
import requests
import time
import typing
import traceback

from textbase import Message
from textbase.utils.utilities import setAPIKeys
from langchain import PromptTemplate, LLMChain
from langchain.chat_models import ChatOpenAI as LangChainOpenAI
from langchain.agents import AgentType, initialize_agent, load_tools

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



class LangChain:
    open_ai_api_key = None
    api_keys = {}

    @classmethod
    def generate(
        cls,
        system_prompt: str,
        message_history: list[Message],
        model="gpt-3.5-turbo",
        max_tokens=1000,
        temperature=0.25,
        max_iterations: int = 5,
        tools: list[str] = ['serpapi', 'wikipedia', 'llm-math'],
    ):
        try:
            assert cls.open_ai_api_key is not None, "OpenAI API key is not set."
            setAPIKeys(cls.api_keys)
            
            chat_history = []

            for message in message_history:
                #list of all the contents inside a single message
                contents = get_contents(message, "STRING")
                if contents:
                    chat_history.extend(contents)

            llm = LangChainOpenAI(
                openai_api_key=cls.open_ai_api_key, 
                temperature=temperature, 
                max_tokens=max_tokens, 
                model_name=model
            )

            tools = load_tools(tools, llm=llm)
            agent = initialize_agent(
                tools, 
                llm, 
                agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, 
                max_iterations=max_iterations,
                verbose=False
            )

            query = chat_history.pop(-1)

            response = agent.run(query['content'])

            if(response == "Agent stopped due to iteration limit or time limit."):
                return "Couldn't find a response to your query."
                
            return response
        except Exception:
            print(f"An exception occured while using this model, please try using another model.\nException: {traceback.format_exc()}.")
            return "Something went wrong."