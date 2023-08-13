import json
import textbase
from textbase.message import Message
from textbase import models
from textbase import nlp
from textbase import githubServices
from textbase import companyServices
from textbase import utils
from textbase import storage
import os
from typing import List

# Load your OpenAI API key
# or from environment variable:
models.OpenAI.api_key = os.getenv("OPENAI_API_KEY")

# Prompt for GPT-3.5 Turbo
SYSTEM_PROMPT = """You are chatting with an AI. There are no specific prefixes for responses, so you can ask or talk about anything you like.
 The AI will respond in a natural, conversational manner. Feel free to start the conversation with any question or topic, and let's have a pleasant chat!
"""

with open("./textbase/constants.json") as json_file:
    constants = json.load(json_file)

async def get_company_interview_questions():
    last_commit =  githubServices.get_github_commits()
    stored_last_commit = await storage.get_data("last_commit")
    if last_commit == stored_last_commit:
        interview_questions_info = githubServices.read_github_file()
        # interview_questions_info = utils.sort(interview_questions_info)
        # await storage.set_data("last_commit",last_commit)
    else:
        company_interview_questions = await storage.get_data("company_interview_questions")
        print("enta unt noduva",company_interview_questions)


    if interview_questions_info is not None:
        ## file content present lets map data into dictionary containing company based interview questions
        # interview_questions_info = utils.sortBasedOnMostOccurence()
        company_interview_questions = companyServices.extract_company_questions(interview_questions_info)
        await storage.set_data("company_interview_questions",company_interview_questions)
    return company_interview_questions

@textbase.chatbot("talking-bot")
async def on_message(message_history: List[Message], state: dict = None):
    """Your chatbot logic here
    message_history: List of user messages
    state: A dictionary to store any stateful information

    Return a string with the bot_response or a tuple of (bot_response: str, new_state: dict)
    """

    if state is None or "counter" not in state:
        state = {"counter": 0}
    else:
        state["counter"] += 1

    company_interview_questions = await get_company_interview_questions()
    if nlp.find_related_question(message_history[-1].content):
            company_names = companyServices.extract_company_names(message_history[-1].content,company_interview_questions)
            if company_names!=[]:
                formated_result = utils.format_question_list(company_interview_questions[company_names[0]],company_names[0])
                return formated_result,state
            else:
                return constants.get("company_not_found"),state

    if (
        len(message_history)>=4
        and nlp.find_related_question(message_history[-3].content)
        and nlp.sort_frequently_asked(message_history[-1].content)
        ):
        return constants.get("already_sorted"),state

    if (
        len(message_history)>=4
        and (nlp.find_related_question(message_history[-3].content)
        or nlp.sort_frequently_asked(message_history[-3].content) 
        and nlp.sort_tag_wise(message_history[-1].content))
        ):
        return constants.get("sorting_not_possible"),state

    if nlp.get_all_companies(message_history[-1].content):
        company_data = companyServices.getCompany(company_interview_questions)
        return utils.format_company_data(company_data),state
     

    # Generate GPT-3.5 Turbo response
    bot_response = models.OpenAI.generate(
        system_prompt=SYSTEM_PROMPT,
        message_history=message_history,
        model="gpt-3.5-turbo",
    )
    return bot_response, state