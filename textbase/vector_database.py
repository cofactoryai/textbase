import weaviate
from textbase import Message,Content
import json
from langchain.vectorstores import Weaviate
from langchain.embeddings.openai import OpenAIEmbeddings

class WeaviateClass:
    api_key = None
    host = None
    auth_key = None
    vector_db_data_class = None
    @classmethod
    def search_in_weaviate(
        cls,
        message_query:Message,
        model_header_key: str,
        max_vector_database_objects: int,
    ):
        assert cls.api_key is not None, "OpenAI API key is not set."
        assert cls.host is not None, "Waaviate Host is not set."
        assert cls.max_weaviate_res_length is not None,"max_weaviate_res_length is not set "
        # auth key is optional so can be skipped for None verification
        weaviate_client = weaviate.Client(
            url = cls.host,
            auth_client_secret=cls.auth_key,
            additional_headers = {
                model_header_key: cls.api_key,
            }
        )
        # take out user query 
        user_query = message_query['content'][0]['value']
        embeddings = OpenAIEmbeddings(
                openai_api_key = cls.api_key
            )

        weaviate_vectorstore = Weaviate(
            weaviate_client,
            cls.vector_db_data_class,
            "text",
            embedding = embeddings
        )
        weaviate_response = weaviate_vectorstore.similarity_search(user_query)
        messages = []
        for response in weaviate_response:
            messages.append(response.page_content)
        
        return   {
            "role": message_query['role'],
            # token limit will exceed so taking limit
            "content": json.dumps(messages,indent=4)[:cls.max_weaviate_res_length]
        }
    

        