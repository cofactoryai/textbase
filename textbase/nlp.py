import spacy

nlp = spacy.load("en_core_web_md")


def nlp_model(user_question,knowledge_base,threshold):
    user_doc = nlp(user_question)
    related_questions = []
    
    for kb_question in knowledge_base:
        kb_doc = nlp(kb_question)
        similarity = user_doc.similarity(kb_doc)

        if similarity > threshold:
            related_questions.append(kb_question)
    
    return True if related_questions else False

def find_related_question(user_question):
    knowledge_base = [
    "Interview questions of ",
    "coding questions of",
    "1st round interview questions "
    ]
    threshold = 0.93
    return nlp_model(user_question,knowledge_base,threshold)

def sort_frequently_asked(user_question):
    knowledge_base = [
    "sort above list ",
    "sort based on frequently asked ",
    "sort based on most asked questions ",
    "sort this",
    "give me frequently asked question"
    ]
    threshold = 0.8
    return nlp_model(user_question,knowledge_base,threshold)

def sort_tag_wise(user_question):
    knowledge_base = [
    "give data structure question",
    "sort based on data structure ",
    "sort based on  difficulty",
    "give me a problem",
    ]
    threshold = 0.93
    return nlp_model(user_question,knowledge_base,threshold)

def get_all_companies(user_question):
    knowledge_base = [
    "list all companies",
    "give all companies ",
    "list companies familiar",
    ]
    threshold = 0.6
    return nlp_model(user_question,knowledge_base,threshold)

    