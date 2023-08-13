
import ast
import json


def format_question_list(question_list,company):
    output = f"\nHere are a few common interview questions that you might encounter when applying for a software development engineering (SDE) position at '{company}':\n\n"

    for idx, pair in enumerate(question_list, start=1):
        url, question_name = pair
        formatted_item = f"{idx}. {question_name}: [{url}]({url})\n\n"
        output += formatted_item
    
    output += "Remember, I'm under training. It's always good to research and prepare for the specific requirements and expectations of the company you're applying to.\n\n"
    print("output",output)
    return output

def sort(interview_questions_info):
    # interview_questions_info = json.load(interview_questions_info)
    data_list = [(url, len(companies)) for url, companies in interview_questions_info.items()]
    sorted_data = sorted(data_list, key=lambda x: x[1], reverse=True)
    sorted_data_dict = {url: interview_questions_info[url] for url, _ in sorted_data}

    return json.dumps(sorted_data_dict, indent=2)

def format_company_data(data_str):
    header = "List of Companies and Number of Questions\n"
    formatted_data = ""
    data = ast.literal_eval(data_str)
    for index, entry in enumerate(data, start=1):
        print(entry,"entry")
        company_name, question_count = entry
        formatted_data += "{}. {}: {} question{}\n".format(
            index, company_name, question_count, "s" if question_count > 1 else ""
        )

    return header + formatted_data 
