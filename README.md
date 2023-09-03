<p align="center">
  <picture>
    <img alt="Textbase python library" src="assets/logo.svg" width="352" height="59" style="max-width: 100%;">
  </picture>
  <br/>
  <br/>
</p>

<h3 align="center">
    <p>✨ Textbase is a framework for building chatbots using NLP and ML. ✨</p>
</h3>

# CHATBOT MOVIE RECOMMENDER

This chatbot is designed to recommend movies and is built on top of the Textbase UI using the provided starter code. It can be seamlessly integrated with OTT platforms like Netflix or Disney Hotstar to offer movie recommendations without users having to search extensively for movies. The implemented features include:

Recommending movies based on genres selected by users.
Recommending movies based on actor or actress names provided by users.
The chatbot's user-friendly interface aims to provide a personalized movie-watching experience by catering to the unique preferences of each user. It simplifies the process of discovering and enjoying movies, ultimately enhancing the overall movie-watching experience.

Additionally, the chatbot has the potential for future expansion and improvement, including the integration of advanced recommendation algorithms and customizable options for users. This chatbot seeks to streamline the movie discovery process and make it more convenient for users to find and enjoy films.

## Implementation

The chatbot is implemented in the following way:
User Input: The chatbot takes user input as its initial step.

- Query Matching: It then checks if the user input matches any predefined queries. These queries likely serve as triggers for specific actions or responses.

- Movie Relatedness: The chatbot determines if the user's input is related to movies. If it's not movie-related, it may provide a generic response or offer assistance with non-movie queries.

- GPT Query: If the input is movie-related, the chatbot sends a query to the GPT model (likely for generating recommendations or responses).

- Movie Recommendations: The GPT model returns a list of movie names based on the user's input, which are potentially related to the user's movie preference or query.

- OMDB API Integration: The chatbot then connects to the OMDB API using these movie names to search for detailed information about the movies, including titles, IMDb URLs, release years, and types.

- Output to User: Finally, the chatbot compiles the movie details obtained from the OMDB API and presents them as recommendations or information to the user.

## Models Used

1. text-davinci-003
2. gpt-3.5-turbo

## Installation

Make sure you have `python version >=3.9.0`, it's always good to follow the [docs](https://docs.textbase.ai/get-started/installation) 👈🏻

### 1. Through pip

```bash
pip install textbase-client
```

### 2. Local installation

Clone the repository and install the dependencies using [Poetry](https://python-poetry.org/) (you might have to [install Poetry](https://python-poetry.org/docs/#installation) first).

For proper details see [here]()

```bash
git clone https://github.com/cofactoryai/textbase
cd textbase
poetry shell
poetry install
```

## Start development server

> If you're using the default template, **remember to set the OpenAI API key** in `main.py`.

Run the following command:

- if installed locally
  ```bash
  poetry run python textbase/textbase_cli.py test
  ```
- if installed through pip
  `bash
textbase-client test
`
  Response:

```bash
Path to the main.py file: textbase/main.py # You can create a main.py by yourself and add that path here. NOTE: The path should not be in quotes
```

## Changes Made

1. The models.py has been updated.
2. The constants.py has been added.
3. The main.py has been added.

## Future Work

There are a lot of improvements that can be done :

- Implementing user customization is a great idea. Allowing users to specify their movie preferences, such as favorite genres, actors, directors, and even movie ratings, can lead to highly personalized movie recommendations.
- Exploring and integrating more advanced movie recommendation models can significantly improve the quality and accuracy of movie suggestions. Models like collaborative filtering, matrix factorization, or deep learning-based recommenders can be considered.
