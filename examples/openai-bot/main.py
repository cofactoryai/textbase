from textbase import bot, Message
from textbase.models import OpenAI
from typing import List
from sentence_transformers import SentenceTransformer, util 
import torch
import requests
# Load your OpenAI API key
OpenAI.api_key = "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"

# Prompt for GPT-3.5 Turbo
SYSTEM_PROMPT = """You are chatting with an AI. There are no specific prefixes for responses, so you can ask or talk about anything you like.
The AI will respond in a natural, conversational manner.
Also, feel free to have real time conversations..Like "Today's weather in India..". AI will give you list of relevant articles
Start the conversation with any question or topic, and let's have a
pleasant chat!
"""
def fetchApiData(new_query): #It's a method to return relevant document urls using semantic search on data fetched from NEWSAPI 
    #relevancy means how much similar is the document fetched from API with the user's query. The more it is similar.. the more is the cosine similarity score
    url = (f'https://newsapi.org/v2/everything?q={new_query}&apiKey=6634b28170f74e08a63cf55841fbf392') #api key is unique
    res = requests.get(url) #retrieving data from NEWSAPI
    json_docs = res.json()
    embedder = SentenceTransformer('bert-base-nli-mean-tokens')
    content_list = []
    url_list = []
    title_list = []
    articles = json_docs['articles']
    for article in articles:
        if article['title'] and article['description']: #if article's title and description are not null
            url_list.append(article['url']) #appending the article's url extracted from json string
            title_list.append(article['title']) #appending article's title 
            content_list.append(article['content'][:200])#appending article's content
        else:
            url_list.append("")
            title_list.append("")
            content_list.append("")
            

    content_list_embeddings = embedder.encode(content_list, convert_to_tensor=True) #converting the article's content to embeddings
    top_k = min(10, len(content_list)) #we need to get top k number of relevant documents - if present
    query_embedding = embedder.encode(new_query, convert_to_tensor=True) #encoding the user query
    cos_scores = util.cos_sim(query_embedding, content_list_embeddings)[0] #computing cosine similarity scores of user query embedding with each article's content embedding
    top_results = torch.topk(cos_scores, k=top_k) #preparing the top k number of relevant results
    final_results = []
    for score, idx in zip(top_results[0], top_results[1]):
        final_results.append(title_list[idx] +"  "+url_list[idx]) #appending the most relevant titles and urls
      

    return final_results

@bot()
def on_message(message_history: List[Message], state: dict = None):

    # Generate GPT-3.5 Turbo response
    
    bot_response = OpenAI.generate(
        system_prompt=SYSTEM_PROMPT,
        message_history=message_history, # Assuming history is the list of user messages
        model="gpt-3.5-turbo",
    )
      
    
    real_time_words = ["today","yesterday","tomorrow","day before yesterday","day after tomorrow","today's","yesterday's","current","last month","this"
                       "live","now","at this moment","present","up-to-date","past","future","next year","next month","last week","last year","next"]
    
    #these are the real time words, which means once these words are found.. they indicate user asks for real time data

    notfound = "false"  
    if "knowledge cutoff"in bot_response or "sorry" in bot_response or "real-time information" in bot_response or "I'm sure there will be more information" in bot_response or "As of my" in bot_response:
        notfound = "true" #if the bot generates a response where it's not able to find the response which users ask..then we set a variable to true
     
    
    user_prompt = message_history[-1]["content"]
    for word in real_time_words:    
        query = str(user_prompt[0]['value']).lower()
        if word in query or notfound=="true": #if user is asking for a real time data or a financial data or latest news after 2021 then this is executed
            new_query = query.strip().replace(" ","%20") #replacing the white spaces in url to %20 before calling the below function
            final_results = fetchApiData(new_query) 
            res = "Here are the top related Articles\n"
            res += "".join("\n"+"\n"+ele+"\n"+"\n" for ele in final_results) #As the final_results is a list.. we convert it to string of urls
            bot_response=res
            break
    
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