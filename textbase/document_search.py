from langchain.text_splitter import SpacyTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.docstore.document import Document
from langchain.vectorstores import FAISS
import PyPDF2
import textbase
from textbase.message import Message
from textbase import models
from typing import List
import os
from dotenv import load_dotenv
load_dotenv()
# Load your OpenAI API key
api_key =  os.environ["OPENAI_API_KEY"]
models.OpenAI.api_key =api_key


class DocumentChat:
    """
    Object for document searching using vector data base. Can be extended to large pdf files.
    The document can contain large contexts as well. 
    """
    
    def __init__(self,binfile,chunk_size=500,chunk_overlap=200):
        self.embeddings_model = OpenAIEmbeddings(openai_api_key=api_key)
        self.text_splitter = SpacyTextSplitter(chunk_size=chunk_size, chunk_overlap = chunk_overlap)
        self.make_doc =  lambda x : Document(page_content=x, metadata={"source": "local"})

        ## query document store
        
        texts = self.read_pdf_file(binfile)
        self.docs = self.make_vecstore(texts)

        self.SYSTEM_PROMPT = lambda x : f"""
            You are a information extractor and your work is to extarct relevant answers
            from the given chunks in response to the query given by the user.

            The context of the document will be provided to you. Answer accordingly.
            Also give the answer in the following format : 
            
            '''
            [
                "answer" : "The inference from the relevant chunk and user query."


                "relevant text from the document to support the answer" : "The part from the text which is contains the answer to the query from the user"
            ]
             '''
            ------------------------------
            Chunks -> 
            {x}
        """
        
    @staticmethod
    def read_pdf_file(pdfFileObj):
        """
        function to convert binary file to readable text string format.
        pdfFileObj : binary file coming from client - pdf
        """
        pdfReader = PyPDF2.PdfReader(pdfFileObj)
        pages = pdfReader.pages
        numpages= len(pages)
        final_text = ""
        for i in range(numpages):
            pageObj = pdfReader.pages[i]
            final_text+= f"{pageObj.extract_text()}\n\n\n" 
        pdfFileObj.close()
        return final_text

    def make_vecstore(self,texts):
        """
        Converts pdf file's text into smaller chunks for smart searching.
        texts : Whole text contained in the document uploaded.

        returns : Text splitted in chunks for futher searching using FAISS
        """
        chunks = self.text_splitter.split_text(texts)
        docs = [self.make_doc(txt) for txt in chunks]
        return FAISS.from_documents(docs, self.embeddings_model)

    def search_for_query(self,query):
        results = self.docs.similarity_search(query,k = 6)
        return "--------xxxxxxx---------".join([doc.page_content for doc in results])

    def get_response(self,query):
        # # Generate GPT-3.5 Turbo response
        chunks = self.search_for_query(query)
        message_history = [Message(content=query,role='user')]
        SYSTEM_PROMPT = self.SYSTEM_PROMPT(chunks)
        bot_response = models.OpenAI.generate(
            system_prompt=SYSTEM_PROMPT,
            message_history=message_history,
            model="gpt-3.5-turbo",
        )
        return bot_response