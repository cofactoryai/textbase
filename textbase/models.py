import openai
import json
import requests

# Need to install this package separately for converting the xml response of TimeTable Lookup API using- 
#   pip install xmltodict 
import xmltodict

from textbase.message import Message

# Util functions for flight data and movie recommendation used in function calling
def flight_info(dest_loc: str, arrival_loc: str, date: str) -> str:
    # API key for TimeTable Lookup API (Free)
    headers = {
        "X-RapidAPI-Key": "a71254c296msh7fdd5b56df1dca6p171241jsnc9294a1b1017",
        "X-RapidAPI-Host": "timetable-lookup.p.rapidapi.com"
    }
    
    # Build the API request URL
    url = "https://timetable-lookup.p.rapidapi.com/TimeTable/{}/{}/{}/"
    url = url.format(arrival_loc, dest_loc, date)
    
    # You can set the number of results you want changing this parameter
    query_string = {'Results': 2}
    response = requests.get(url, headers=headers, params=query_string)

    # print(response.text)
    
    # Return the flight information by converting the xml response into json using xmltodict package
    return json.dumps(xmltodict.parse(response.text))

def movie_recommendation(user_input: str) -> str:
    # API key for The Movie Database (TMDb)
    api_key = "fc4019ab5cea82a5f67c777e2c9aa81a"

    # Build the API request URL
    url = f"https://api.themoviedb.org/3/search/multi?api_key={api_key}&query={user_input}&language=en-US"

    # Retrieve the movie data from the API
    response = requests.get(url)
    data = json.loads(response.content)
    recommended_movie = data["results"][0]

    # Return the movie information
    return json.dumps(recommended_movie)

class OpenAI:
    api_key = None

    @classmethod
    def generate(
        cls,
        system_prompt: str,
        message_history: list[Message],
        model="gpt-3.5-turbo",
        max_tokens=3000,
        temperature=0.7,
    ):
        assert cls.api_key is not None, "OpenAI API key is not set"
        openai.api_key = cls.api_key

        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                *map(dict, message_history),
            ],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response["choices"][0]["message"]["content"]
    
    # Custom function for integrating movie recommender and flight detail guide features to our chatbot
    @classmethod
    def generate_custom(cls,
        system_prompt: str,
        message_history: list[Message],
        model="gpt-3.5-turbo",
        max_tokens=1000,
        temperature=0.7,
    ):
        assert cls.api_key is not None, "OpenAI API key is not set"
        openai.api_key = cls.api_key
        
        messages=[
            {"role": "system", "content": system_prompt},
            *map(dict, message_history),
        ]
        
        # Adding function list
        functions = [
            {
                "name": "movie_recommendation",
                "description": "Get movie details for a movie",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Film's name, actor's name, director's name, genre, language or release date of movie",
                        }                    
                    },
                    "required": ["name"],
                },
            },
            {
                "name": "flight_info",
                "description": "Get list of upcoming flight details from one airport to another",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "dest": {
                            "type": "string",
                            "description": "Destination airport IATA eg: CCU, BLR, etc.",
                        },
                        "arriv": {
                            "type": "string",
                            "description": "Arrival airport IATA eg: DEL, BOS, etc.",
                        },
                        "date": {
                            "type": "string",
                            "description": "Date of flight in YYYYMMDD format eg: 20230731",
                        }                      
                    },
                    "required": ["dest", "arriv", "date"],
                },
            }
        ]
        
        # Implementing function calling
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            functions=functions,
            function_call="auto",
        )
        response_message = response["choices"][0]["message"]

        # Check if GPT wanted to call a function
        if response_message.get("function_call"):
            # Call the function
            available_functions = {
                "movie_recommendation": movie_recommendation,
                "flight_info": flight_info,
            }  # only two functions in this example, but you can have more
            
            function_name = response_message["function_call"]["name"]
            function_to_call = available_functions[function_name]
            function_args = json.loads(response_message["function_call"]["arguments"])
            
            if function_name == "flight_info":
                function_response = function_to_call(
                    dest_loc=function_args.get("dest"),
                    arrival_loc=function_args.get("arriv"),
                    date=function_args.get("date"),
            )
            elif function_name == "movie_recommendation":
             function_response = function_to_call(
                user_input=function_args.get("name"),
            )

            # Send the info on the function call and function response to GPT
            messages.append(response_message)  # extend conversation with assistant's reply
            messages.append(
                {
                    "role": "function",
                    "name": function_name,
                    "content": function_response,
                }
            )  # extend conversation with function response
            
            second_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0613",
                messages=messages,
            )  # get a new response from GPT where it can see the function response
            
            return second_response["choices"][0]["message"]["content"]
        
        # If no relevant keywords found for the 2 functions return normal GPT3.5 response
        else:            
            return response["choices"][0]["message"]["content"]
