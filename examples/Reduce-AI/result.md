# Shortening Open API Usage and Enhancing User-Friendly Interactions

## Overview

In this project, we aim to optimize the usage of Open API and improve the user experience by leveraging a pre-trained chatbot dataset. By converting the dataset into a CSV file, we can create a streamlined interaction process, reducing the dependence on Open API while enhancing user-friendliness.

## Objectives

- Utilize a pre-trained chatbot dataset from Kaggle.
- Convert the dataset into a CSV file for easy processing.
- Implement a decision-making process for user queries based on relevance.
- Shorten Open API usage when answering user questions.
- Enhance the product's user-friendliness by providing context-specific responses.

## Approach

1. **Dataset Conversion**: We begin by converting the pre-trained chatbot dataset into a CSV file. This format allows us to efficiently manage and manipulate the data.

2. **Relevance Check**: When a user query is received, the system checks if the query is related to legal matters. If so, the system directly routes the query to the Open API for an accurate response.

3. **TF-IDF and Cosine Similarity**: If the query is not related to legal matters, the system processes the query using TF-IDF and cosine similarity. The CSV file, containing pre-existing chat responses, is vectorized using TF-IDF. The cosine similarity is then calculated to find the most relevant response based on user input.

4. **Sentiment Analysis**: If the cosine similarity-based search fails to find a relevant response, the system performs sentiment analysis on the query. If the sentiment is positive or neutral, the system prompts the user to provide more context. If the sentiment is negative, the system requests further clarification.

## Implementation

```python
# Pseudocode for handling user queries

if query_related_to_legal(input_query):
    response = Open_API.get_response(input_query)
else:
    query_vector = tfidf_vectorizer.transform([input_query])
    similarities = cosine_similarity(query_vector, tfidf_matrix)
    
    if max(similarities) > similarity_threshold:
        most_similar_index = similarities.argmax()
        response = csv_data[most_similar_index]
    else:
        sentiment = perform_sentiment_analysis(input_query)
        if sentiment == "positive" or sentiment == "neutral":
            response = "Please provide more context."
        else:
            response = "I can't understand what you're saying. Please elaborate."

return response
```

## Results

By implementing this approach, we achieved the following outcomes:

- **Reduced Open API Usage**: The majority of non-legal queries are now handled internally through the dataset and cosine similarity search, reducing the burden on Open API calls.

- **Enhanced User-Friendly Interaction**: Users receive more contextually relevant responses, leading to a smoother and more user-friendly experience.

- **Optimized Product Performance**: The system efficiently decides whether to use Open API or the internal dataset, leading to better performance and reduced latency.

## Screenshots



## Conclusion

By leveraging a pre-trained chatbot dataset and implementing a strategic decision-making process, we have successfully shortened the Open API usage and improved the user experience. This project demonstrates the potential for enhanced product efficiency and user satisfaction through thoughtful design and implementation.