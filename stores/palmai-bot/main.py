from textbase import bot, Message
import google.generativeai as palm
from typing import List
import chromadb
from chromadb.api.types import Document, Embeddings

palm.configure(api_key='')

DOCUMENT = "Textbase is an awesome app"


def embed_function(texts: Document) -> Embeddings:
    return [palm.generate_embeddings(model='models/embedding-gecko-001', text=text)['embedding']
            for text in texts]


def create_chroma_db(documents, name):
    chroma_client = chromadb.Client()
    db = chroma_client.create_collection(
        name=name, embedding_function=embed_function)
    for i, d in enumerate(documents):
        db.add(
            documents=d,
            ids=str(i)
        )
    return db


db = create_chroma_db([DOCUMENT], "textbasedb")


def get_relevant_passage(query, db):
    passage = db.query(query_texts=[query], n_results=1)['documents'][0][0]
    return passage


def make_prompt(query, relevant_passage):
    escaped = relevant_passage.replace(
        "'", "").replace('"', "").replace("\n", " ")
    prompt = ("""You are a helpful and informative bot that answers questions using text from the reference passage included below. \
  Be sure to respond in a complete sentence, being comprehensive, including all relevant background information. \
  However, you are talking to a non-technical audience, so be sure to break down complicated concepts and \
  strike a friendly and converstional tone. \
  If the passage is irrelevant to the answer, you may ignore it.
  QUESTION: '{query}'
  PASSAGE: '{relevant_passage}'

    ANSWER:
  """).format(query=query, relevant_passage=escaped)

    return prompt


@bot()
def on_message(message_history: List[Message], state: dict = None):

    query = message_history[-1]['content'][0]['value']
    passage = get_relevant_passage(query, db)
    prompt = make_prompt(query, passage)

    bot_response = palm.generate_text(
        prompt=prompt,
        model="models/text-bison-001",
        temperature=0.65,
        max_output_tokens=1000
    )

    bot_response = bot_response.candidates[0]['output']

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
