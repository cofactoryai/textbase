Integrating NewsAPI to fetch Real-time, Financial and latest data using Semantic search with SentenceTransformers


This pull request is made to make the bot more user friendly. Now, this bot can provide answers dealing with real time data, 
financial data and latest news after 2019, which an openAI bot cannot answer. This bot handles the limitations of Generic OpenAI bot

Strategy Used:

1. I integrated a 3rd party NewsAPI to extract the latest up to date news in the form json strings
2. After extracting all the news articles, I used semantic search with sentenceTransformers, with which we can semantically search
for the most similar or relavent document to the user's query. 
3. Then I ranked the top kth relevant documents based on cosine similarity scores
4. The user will be able to view the document Titles and URLs whenever he asks for real time or financial or latest news that an OpenAI
cannot answer

Libraries Installed
1. installed SentenceTransformers library for semantic search 
2. Integrated NewsAPI with a unique api key that one can freely obtain after logging onto NewsAPI website