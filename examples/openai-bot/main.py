from langchain import LLMChain
from textbase import bot, Message
from textbase.models import OpenAI
from typing import List
from langchain.llms import OpenAI as LangOpenAI
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.utilities import WikipediaAPIWrapper

# Set your LangChain API key
langchain_api_key = 'YOUR_LANGCHAIN_API_KEY'

# Initialize LangChain components
llm = LangOpenAI(api_key=langchain_api_key, temperature=0.9)
title_template = PromptTemplate(
    input_variables=['topic'],
    template='Get me important notes from youtube for the topic known as {topic}'
)
title_memory = ConversationBufferMemory(
    input_key='topic', memory_key='chat_history'
)
wiki = WikipediaAPIWrapper()

# Load your OpenAI API key for TextBase
OpenAI.api_key = ""

# Prompt for GPT-3.5 Turbo
SYSTEM_PROMPT = """
Welcome to the YouTube Content and Title Generator Chatbot!
I'm here to help you come up with creative YouTube video ideas and titles.
Please choose one of the following options or provide specific prompts:
1. Generate video ideas based on a topic or keyword.
2. Suggest catchy video titles for your content.
3. Combine multiple topics for unique video concepts.
4. Request video ideas tailored to your audience.
5. Ask for tips on optimizing YouTube video titles and descriptions.
6. Something else (Feel free to ask any YouTube-related question or request).
"""

@bot()
def on_message(message_history: List[Message], state: dict = None):
    user_message = message_history[-1].text

    # Check if the user requests YouTube content or titles
    if "generate YouTube content" in user_message.lower():
        # Extract the topic from the user's message
        topic = user_message.split("generate YouTube content")[1].strip()
        
        # Call LangChain to generate YouTube content
        title_chain = LLMChain(llm=llm, prompt=title_template,
                               verbose=True, output_key='title', memory=title_memory)
        script_chain = LLMChain(llm=llm, prompt=script_template,
                                verbose=True, output_key='script', memory=script_memory)
        
        # Generate title and research using LangChain
        title = title_chain.run({"topic": topic})
        wiki_research = wiki.run({"topic": topic})
        
        # You can format and return the generated content as needed
        generated_content = f"Title: {title}\nWikipedia Research: {wiki_research}"
        
        bot_response = generated_content
    else:
        # Generate GPT-3.5 Turbo response based on SYSTEM_PROMPT
        bot_response = OpenAI.generate(
            system_prompt=SYSTEM_PROMPT,
            message_history=message_history,  # Assuming history is the list of user messages
            model="gpt-3.5-turbo",
        )

    response = {
        "data": {
            "messages": [
                {
                    "data_type": "STRING",
                    "value": bot_response
                }
            ],
            "state": state
        },
        "errors": [
            {
                "message": ""
            }
        ]
    }

    return {
        "status_code": 200,
        "response": response
    }
