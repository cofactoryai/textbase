from textbase import bot, Message
from textbase.models import OpenAI
from typing import List

# Load your OpenAI API key
OpenAI.api_key = ""

# Prompt for GPT-3.5 Turbo
SYSTEM_PROMPT = """Employee Training Mentor; Lets create a chatbot that helps with employee training and onboarding. It will be able to provide training modules answer employee questions and keep track of progress making the learning process smooth and efficient.
Step1: We'll start by developing a module that introduces employees to the companys culture, mission and values. This module will give them insights, into the organizations history and core principles.
Step2: Next we'll design a module for job related training. The chatbot will deliver this content in an interactive manner, including quizzes and assessments to gauge understanding.
Step3: To make it more user friendly we'll implement a natural language understanding system so that employees can ask questions about policies, procedures or anything else related to their role. The chatbot will always provide up to date information.
Step4: In addition to delivering training content we'll develop a feature that tracks employees progress as they complete modules, quizzes and assessments. The chatbot will generate reports. Offer feedback to both employees and supervisors.
Step5: To cater to learning styles such, as auditory or kinesthetic preferences of individuals. we'll ensure that the chatbot can adapt accordingly by recommending learning materials.
Step6: Lastly but importantly we will prioritize data security and privacy when handling employee information as their training records.
Ensure the implementation of security protocols to safeguard information.
Utilize this prompt as a reference to shape the creation of the Employee Training Mentor chatbot with an emphasis, on establishing an efficient onboarding and training process, for newly hired individuals.
"""

@bot()
def on_message(message_history: List[Message], state: dict = None):

    # Generate GPT-3.5 Turbo response
    bot_response = OpenAI.generate(
        system_prompt=SYSTEM_PROMPT,
        message_history=message_history, # Assuming history is the list of user messages
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