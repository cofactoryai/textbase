from textbase import bot, Message
from textbase.models import OpenAI
from typing import List
import chromadb
from chromadb.api.types import Document, Embeddings
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction

OpenAI.api_key = ""

DOCUMENT = "Textbase is an awesome app"

embed_function = OpenAIEmbeddingFunction(OpenAI.api_key)


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

    bot_response = OpenAI.generate(
        system_prompt=prompt,
        message_history=message_history,
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
