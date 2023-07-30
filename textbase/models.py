import openai

from textbase.message import Message


class OpenAI:
    def __init__(self, api_key=None) -> None:
        self.api_key = api_key


    def set_api_key(self, api_key) -> None:
        """`set_api_key` method allows user to set or update API keys dynamically."""
        self.api_key = api_key

    def generate(
        self,
        system_prompt: str,
        message_history: list[Message],
        model="gpt-3.5-turbo",
        max_tokens=3000,
        temperature=0.7,
    ):
        if self.api_key is None:
            raise ValueError("OPENAI API key is not set")
        openai.api_key = self.api_key

        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                *map(dict, message_history),
            ],
            temperature=temperature,
            max_tokens=max_tokens,
        )

        if "choices" in response and response["choices"]:
            return response["choices"][0]["message"]["content"]
        else:
            raise RuntimeError("Failed to generate response. Checkout API key and parameters")