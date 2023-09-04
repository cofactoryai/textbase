import os
import datetime
import logging
from textbase import bot, Message
from textbase.models import LangchainBot
from typing import List
from langchain.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import CharacterTextSplitter
import pickle
from langchain.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain.embeddings import SentenceTransformerEmbeddings

from langchain import OpenAI as LangOpenAI
from langchain.chains import RetrievalQA
from langchain.memory import ConversationBufferWindowMemory


os.environ["OPENAI_API_KEY"] = "api-key"

'''A chatbot with Integration of Langchain and OpenAI to do a domain specific task and get the latest 
   data as required throught approapriate channels
   This also includes the usages of Faiss vector stores https://github.com/facebookresearch/faiss
   to perform the similarity search in accordance to the embedded vectors '''

'''We can modify these urls according to our target topic and also make sure these websites are bot freindly
 Hereby choosing a finance oriented task to get the latest news on stocks or markets you are intereseted'''

prompt_template = """Use the latest yahoo data to answer the question and integrate it with some of your past intelligence
to give insights and don't try to make up an answer.

{context}

Question: {question}
"""
PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)

# Configure the logging settings
logging.basicConfig(filename='lanchain-bot.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')

#specify the url
urls = ['https://finance.yahoo.com/news/']
logging.info(f"Urls used {urls}")

''' Creating this function to avoid excessive usage of OpenAI service 
    for free accounts & can modify according to paid plans '''

def process_url_and_save_embeddings(urls):
    logging.info("Data retreival , embedding and Vector store method called")
    # Load files from the remote URL
    loaders = UnstructuredURLLoader(urls=urls)
    data = loaders.load()

    # Text Splitter
    text_splitter = CharacterTextSplitter(separator='\n',
                                          chunk_size=1000,
                                          chunk_overlap=0)

    docs = text_splitter.split_documents(data)

    # Convert words into embeddings
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

    # Provides a function to search in them with L2 and/or dot product vector comparison
    vectorStore_openAI = FAISS.from_documents(docs, embeddings)
    logging.info("vectorstore updated")

    # Save the embeddings to a pickle file
    with open("faiss_store_openai.pkl", "wb") as f:
        pickle.dump(vectorStore_openAI, f)

    return vectorStore_openAI     
          

''' Updates Vector store at 7 am for fresh market updates '''
now = datetime.datetime.now()
if now.hour == 7:
 VectorStore = process_url_and_save_embeddings(urls)
 logging.info("Data saved to pickle file at 7 am")
    
#load the file contents for Initial setup
with open("faiss_store_openai.pkl", "rb") as f:
    VectorStore = pickle.load(f) 

@bot()
def on_message(message_history: List[Message], state: dict = None, prompt = PROMPT,vector = VectorStore.as_retriever()):

    # Generate GPT-3.5 Turbo response
    bot_response = LangchainBot.generate(
        prompt=prompt,
        message_history=message_history, # Assuming history is the list of user messages
        vector =  vector
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



'''
Code for the models.py


from langchain import OpenAI as LangOpenAI
from langchain.chains import RetrievalQA
from langchain.memory import ConversationBufferWindowMemory

class LangchainBot:
    api_key = None
    #os.environ["OPENAI_API_KEY"] = "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"
    @classmethod
    def generate(
        cls,
        message_history: list[Message],
        temperature=0.7, prompt = None ,vector = None
    ):
        assert cls.api_key is not None, "OpenAI API key is not set."
        #LangOpenAI.api_key = cls.api_key

        #Creating model        
        llm = LangOpenAI(temperature=temperature)    

        #will store upto past 5 conversations, Imp feature for chatbots
        memory = ConversationBufferWindowMemory( k=5) 

        #chain for outputs 
        chain_type_kwargs = {"prompt": prompt }
        qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever= vector, memory = memory, chain_type_kwargs=chain_type_kwargs)

        query = message_history[-1]["content"]["value"]
        response = qa.run(query)
        
        return response 
        
        '''