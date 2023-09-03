from pickle import TRUE
import openai
import requests
import re
from textbase import Message
from constants import *

# Global constants


# Global Methods


def get_contents(message: Message, data_type: str) -> list:
    """
    Get contents of a specific data_type from a message.
    """

    return [
        {
            "role": message["role"],
            "content": content["value"]
        }
        for content in message["content"]
        if content["data_type"] == data_type
    ]


def recommendMovies(genre: str) -> str:
    """
    Recommend movies based on genre using the OMDB API.
    """

    omdb_api_key = "95c3af0b"
    omdb_url = f"http://www.omdbapi.com/?s={genre}&apikey={omdb_api_key}"
    print(omdb_url)
    response = requests.get(omdb_url)
    print(response)
    data = response.json()
    recommended_movies = []
    if "Search" in data:
        for movie in data["Search"]:
            print(movie)
            title = movie.get("Title", "")
            imdb_id = movie.get("imdbID", "")
            year = movie.get("Year", "")
            type = movie.get("Type", "")
            imdb_url = f"https://www.imdb.com/title/{imdb_id}/"
            recommended_movies.append({
                "title": title,
                "imdb_url": imdb_url,
                "year": year,
                "type": type,
            })
    return recommended_movies


class OpenAI:
    api_key = None

    @classmethod
    def checkStatementIsRelatedToMovie(cls, user_message):
        """
        gpt model to check if the input text is related to movies
        """

        if (any(keyword in user_message for keyword in yesNoQuestionList)):
            return TRUE

        if (any(keyword in user_message for keyword in genres)):
            return TRUE

        # Define a prompt to frame your question
        prompt = f"{BASE_PROMPT} '{user_message}'"

        # Use GPT-3.5 Turbo to check if the sentence is related to movies
        response = openai.Completion.create(
            engine="text-davinci-003",  # You can use GPT-3.5 Turbo for faster results
            prompt=prompt,
            max_tokens=1,  # Set max_tokens to 1 to get a brief answer
        )
        print(response)
        # Check the model's completion for a relevant response
        is_related_to_movies = "yes" in response.choices[0].text.lower()
        print(is_related_to_movies)
        return is_related_to_movies

    @classmethod
    def generate(
        cls,
        system_prompt: str,
        message_history: list[Message],
        model="gpt-3.5-turbo",
        max_tokens=1000,
        temperature=0.7,
    ):
        assert cls.api_key is not None, "OpenAI API key is not set."
        openai.api_key = cls.api_key
        user_message = user_message = message_history[-1]["content"][0]["value"].lower(
        )
        filtered_messages = []

        if any(keyword in user_message for keyword in suggestionKeywordList):
            return SUGGEST_KEYWORD_PROMPT

        if any(keyword in user_message for keyword in whoKeywordList):
            return WHO_KEYWORD_PROMPT

        if any(keyword in user_message for keyword in howKeywordList):
            return HOW_KEYWORD_PROMPT

        if any(keyword in user_message for keyword in whatKeywordList):
            return WHAT_KEYWORD_PROMPT

        if any(keyword in user_message for keyword in welcomeKeywordList):
            return WELCOME_KEYWORD_PROMPT

        if cls.checkStatementIsRelatedToMovie(user_message) == TRUE:
            for message in message_history:
                # list of all the contents inside a single message
                contents = get_contents(message, "STRING")
                if contents:
                    filtered_messages.extend(contents)
            response = openai.ChatCompletion.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    *map(dict, filtered_messages),
                ],
                temperature=temperature,
                max_tokens=max_tokens,
            )
            result = response["choices"][0]["message"]["content"]
            pattern = r'"([^"]+)"'
            movie_names = re.findall(pattern, result)
            recommended_movies_list = []
            for name in movie_names:
                recommended_movies = recommendMovies(name)
                recommended_movies_list.append(recommended_movies)
            if recommended_movies_list:
                response = "Here are some movie recommendations for you:\n\n"
                for movies in recommended_movies_list:
                    for index, movie in enumerate(movies):
                        response += f"● Recommended Movie - {index + 1}\n\n"
                        response += f" Title: {movie['title']}\n\n"
                        response += f" IMDb URL: {movie['imdb_url']}\n\n"
                        response += f" Release Year: {movie['year']}\n\n"
                        response += f" Type: {movie['type']}\n\n"
                return response
            if result:
                return result
            else:
                return MOVIE_NOT_FOUND_PROMPT

        else:
            return NOT_RELATED_MOVIE_PROMPT
