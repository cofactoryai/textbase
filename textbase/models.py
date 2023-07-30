import openai

from textbase.message import Message

import json
from EdgeGPT.EdgeGPT import Chatbot, ConversationStyle
from EdgeGPT.ImageGen import ImageGen
import argparse
from EdgeGPT.ImageGen import ImageGenAsync
import requests

class OpenAI:
    api_key = None

    @classmethod
    def generate(
        self,
        system_prompt: str,
        message_history: list[Message],
        model="gpt-3.5-turbo",
        max_tokens=3000,
        temperature=0.7,
    ):
        assert self.api_key is not None, "OpenAI API key is not set"
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
        return response["choices"][0]["message"]["content"]
    
    @classmethod
    async def generate_using_Edge(
        self,
        system_prompt: str,
        message_history: Message,
    ):
        cookies = json.loads(open("textbase/cookies.json", encoding="utf-8").read())
        bot = await Chatbot.create(cookies=cookies)
        response = await bot.ask(prompt=message_history.content, conversation_style=ConversationStyle.creative, simplify_response=True)
        return json.dumps(response, indent=2)

    # @classmethod
    # async def generate_image_using_Edge(
    #     self,
    #     system_prompt: str,
    #     message_history: Message,
    # ):
    #     parser = argparse.ArgumentParser()
    #     parser.add_argument("-U", help="Auth cookie from browser", type=str)
    #     parser.add_argument(
    #     "--output-dir",
    #     help="Output directory",
    #     type=str,
    #     default="textbase/static",
    #     )
    #     parser.add_argument(
    #     "--quiet", help="Disable pipeline messages", action="store_true"
    #     )
    #     parser.add_argument(
    #     "--prompt",
    #     help="Prompt to generate images for",
    #     type=str,
    #     required=True,
    #     )
    #     args = parser.parse_args()

    #     args.prompt = message_history.content  
    #     cookie_json = json.loads(open("textbase/cookies.json", encoding="utf-8").read())
    #     for cookie in cookie_json:
    #         if cookie.get("name") == "_U":
    #             args.U = cookie.get("value")
    #             break
    #     async with ImageGenAsync(args.U, args.quiet) as image_generator:
    #         print(args.prompt)
    #         images = await image_generator.get_images(args.prompt)
    #         print(images)
    #         await image_generator.save_images(images, output_dir=args.output_dir)
    #     return "done"

    # @classmethod
    # async def analyse_text_recognant(
    #     self,
    #     system_prompt: str,
    #     message_history: Message,
    # ):
    #     url = "https://nlp-nlu.p.rapidapi.com/superstring/"
    #     payload = {
    #     	"q": message_history.content,
    #     	"m": "tokencount,composition"
    #     }
    #     headers = {
    #     	"content-type": "application/x-www-form-urlencoded",
    #     	"X-RapidAPI-Key": "fc4c22ae66mshd9319d676b1e78cp199e28jsn7f06732ddd50",
    #     	"X-RapidAPI-Host": "nlp-nlu.p.rapidapi.com"
    #     }
    #     response = requests.post(url, data=payload, headers=headers)
    #     print(response.json())
    #     return "done"