import re
import json

def extract_company_questions(data):
    company_interview_questions = {}
    # Dictionary to store company names as keys and a list of questions as values
    parsed_data = json.loads(data)
    for url, companies in parsed_data.items():
        question_name = companies[0].lower().strip()
        for company_data in companies[1:]:
            company_name = company_data.lower().strip()
            
            if company_name not in company_interview_questions:
                company_interview_questions[company_name] = []

            company_interview_questions[company_name].append((url, question_name))
    return company_interview_questions

def extract_company_names(message,company_interview_questions):
    company_names = []
    for company in company_interview_questions:
        pattern = re.compile(r'\b' + re.escape(company.lower()) + r'\b')
        if re.search(pattern, message.lower()):
            company_names.append(company)
    
    return company_names

def getCompany(company_interview_questions):
    available_companies = []
    # print("company_interview_questions",company_interview_questions,"company_interview_questions")
    for company in company_interview_questions:
        questions = company_interview_questions[company]
        available_companies.append((company, len(questions)))
    return json.dumps(available_companies)

# def mergeCommonQuestions(company_interview_questions,company_names):
#     # //for common questions
#     common_questions = {}
#     for company in company_names:
#         # //this is to store company specific question
#         company = {}
#     # company_interview_questions is a dictionary key as company name
#     # and value as list of pair (url,question_name)
#     # my task is to seperate company having same questions into common question
#     # and company specific questions in company dictionary - not priority
    
