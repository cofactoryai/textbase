import openai
import os
from dotenv import load_dotenv

load_dotenv()

class GPT3Chatbot:
    def __init__(self, 
                 model="gpt-3.5-turbo", 
                 system_prompt="You are a helpful assistant.", 
                 temperature=0.7, 
                 max_tokens=256, 
                 n=1, 
                 presence_penalty=0, 
                 frequency_penalty=0.1):
        """
        generate_gpt_response - Generates text using the OpenAI API.
        :param str prompt: prompt for the model
        :param str openai_api_key: api key for the OpenAI API, defaults to None
        :param str model: model to use, defaults to "gpt-3.5-turbo"
        :param str system_prompt: initial prompt for the model, defaults to "You are a helpful assistant."
        :param float temperature: _description_, defaults to 0.5
        :param int max_tokens: _description_, defaults to 256
        :param int n: _description_, defaults to 1
        :param Optional[Union[str, list]] stop: _description_, defaults to None
        :param float presence_penalty: _description_, defaults to 0
        :param float frequency_penalty: _description_, defaults to 0.1
        :return List[str]: _description_
        """
        self.model = model
        self.system_prompt = system_prompt
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.n = n
        self.presence_penalty = presence_penalty
        self.frequency_penalty = frequency_penalty

        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        assert self.openai_api_key is not None, "OpenAI API key not found."

    def generate_gpt_response(self, prompt):
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": prompt},
        ]

        openai.api_key = self.openai_api_key

        response = openai.ChatCompletion.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            n=self.n,
            presence_penalty=self.presence_penalty,
            frequency_penalty=self.frequency_penalty,
        )

        generated_texts = [
            choice.message["content"].strip() for choice in response["choices"]
        ]
        return generated_texts


 