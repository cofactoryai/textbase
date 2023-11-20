from textbase import bot, Message
from typing import List
import pandas as pd
import matplotlib
matplotlib.use('agg')
from pandasai import PandasAI
import os
from pandasai.llm.openai import OpenAI


#os.environ['OPENAI_API_KEY']="sk-****"
df=pd.read_csv("C:/Users/varun/Documents/vscode python/USA_cars_datasets.csv")  #sample csv file

@bot()
def on_message(message_history: List[Message], state: dict = None):

    #read csv file as pandas dataframe when user uploads a file:- df=pd.read_csv("C:/Users/varun/Documents/vscode python/USA_cars_datasets.csv")
   
    llm=OpenAI(temperature=0)
    pandas_ai=PandasAI(llm=llm,conversational=True,save_charts=True)      
    res=pandas_ai.run(df,prompt=message_history[-1]["content"][0]["value"])  
    bot_response = [{"data_type":"STRING","value":str(res)}]  
   
    response = {
        "data": {
            "messages": bot_response,
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