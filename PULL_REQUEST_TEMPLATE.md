![textbase_screenshot4_realtime_2](https://github.com/Jeevana38/textbase/assets/77659039/7a116ebd-afdb-4804-9672-5ac5819e4a7d)
![textbase_screenshot3_realtimeweather_1](https://github.com/Jeevana38/textbase/assets/77659039/111ca022-763a-4bb4-b92c-ffb8a636dd5b)
![textbase_screenshot2_financialnews](https://github.com/Jeevana38/textbase/assets/77659039/0cfa7620-2d2b-46b7-a809-3dc3b7332b40)
![textbase_screenshot1_latestnews](https://github.com/Jeevana38/textbase/assets/77659039/6ffa52a4-ce63-4c22-9eb3-10f34fb93aba)
## Scope
Integrating NewsAPI to fetch Real-time, Financial, and latest data using Semantic search with SentenceTransformers


This pull request is made to make the bot more user-friendly. Now, this bot can provide answers dealing with real-time data, 
financial data and latest news after 2019, which an openAI bot cannot answer. This bot handles the limitations of the Generic OpenAI bot

Strategy Used:

1. I integrated a 3rd party NewsAPI to extract the latest up-to-date news in the form json strings
2. After extracting all the news articles, I used semantic search with sentenceTransformers, with which we can semantically search
for the most similar or relevant document to the user's query. 
3. Then I ranked the top kth relevant documents based on cosine similarity scores
4. The user will be able to view the document Titles and URLs whenever he asks for real-time or financial or latest news that an OpenAI
cannot answer

Libraries Installed
1. Installed SentenceTransformers library for semantic search 
2. Integrated NewsAPI with a unique API key that one can freely obtain after logging onto the NewsAPI website



- [ ] `[Sub task]`


### Screenshots
---Attached screenshots in examples --> openai-bot -- > screenshots (folder)


## Code improvements
- Added functionality with which the bot is able to answer Real-Time queries, Financial data, and latest news
with the help of NewsAPI integration using SentenceTransformers semantic search


### Developer checklist
- [ ] I’ve manually tested that code works locally on desktop and mobile browsers.
- [ ] I’ve reviewed my code.
- [ ] I’ve removed all my personal credentials (API keys etc.) from the code.
