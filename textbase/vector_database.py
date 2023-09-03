import weaviate
from textbase import Message,Content
import json
from langchain.vectorstores import Weaviate
from langchain.embeddings.openai import OpenAIEmbeddings

class WeaviateClass:
    @classmethod
    def search_in_weaviate(
        cls,
        api_key: str,
        host: str,
        auth_key:str,
        weaviate_data_class,
        message_query:Message,
        max_weaviate_res_length: int,
        model_header_key: str,
    ):
        weaviate_client = weaviate.Client(
            url = host,
            auth_client_secret=auth_key,
            additional_headers = {
                model_header_key: api_key,
            }
        )
        # take out user query 
        user_query = message_query['content'][0]['value']
        embeddings = OpenAIEmbeddings(
                openai_api_key = api_key
            )

        weaviate_vectorstore = Weaviate(
            weaviate_client,
            weaviate_data_class,
            "text",
            embedding = embeddings
        )
        weaviate_response = weaviate_vectorstore.similarity_search(user_query)
        messages = []
        for response in weaviate_response:
            messages.append(response.page_content)
        response_string = json.dumps(messages)
        
        # if token limit exceed error come user can configure max_weaviate_res_length to be considered for output
        if max_weaviate_res_length  and len(response_string)>max_weaviate_res_length :
            response_string = response_string[:max_weaviate_res_length]
        return  response_string
    

        