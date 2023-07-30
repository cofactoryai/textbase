import openai
from textbase.logger import log_it,LOG_ERROR
from textbase.message import Message
from typing import List

class OpenAI:
    api_key = None

    @classmethod
    def generate(
        cls,
        system_prompt: str,
        message_history: List[Message],
        model="gpt-3.5-turbo",
        max_tokens=3000,
        temperature=0.7,
    ):
        try:
            assert cls.api_key is not None, "OpenAI API key is not set"
            openai.api_key = cls.api_key

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
        except openai.error.AuthenticationError as e:
            #handle incorrect API key error
            error_message = "Incorrect API key is provided .Please check your API Key and ensure it is correct"
            log_it(error_message,LOG_ERROR)
        except openai.error.RateLimitError as e:
            #handle rate limit error
            error_message = "You exceeded your current quota, please check your plan and billing details."
            log_it(error_message,LOG_ERROR)
        except Exception as e:
            log_it(f"Exception in generate method ",LOG_ERROR)
