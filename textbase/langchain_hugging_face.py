import typing
import textbase
from textbase.message import Message
from typing import List
from langchain import HuggingFaceHub
from langchain import PromptTemplate, LLMChain
from langchain.memory import ConversationBufferMemory
# get a token: https://huggingface.co/docs/api-inference/quicktour#get-your-api-token

import os
api_key = "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"
os.environ["HUGGINGFACEHUB_API_TOKEN"] = api_key

@textbase.chatbot("talking-bot")
def generate(
    system_prompt: str,
    model: typing.Optional[str] = "databricks/dolly-v2-3b",
    max_tokens: typing.Optional[int] = 100,
    temperature: typing.Optional[float] = 0.9,
    min_tokens: typing.Optional[int] = None,
    top_k: typing.Optional[int] = 50
    ) -> str:
        try:
            assert api_key is not None, "Hugging Face API key is not set"

            hub_llm = HuggingFaceHub(repo_id="databricks/dolly-v2-3b", model_kwargs={"temperature": temperature, "max_length": max_tokens, "top_k": top_k})

            template = """Chat with me, {system_prompt}
            """
            prompt = PromptTemplate(template=template, input_variables=["system_prompt"])
            llm_chain = LLMChain(prompt=prompt, llm=hub_llm, verbose=True)
            
            response = llm_chain.run(system_prompt)
            
            
            return response
        except Exception as ex:
            print(f"Error occured while using this model, please try using another model, Exception was {ex}")

print(generate("What is the best thing about life?"))