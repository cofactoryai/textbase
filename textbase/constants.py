# Global Variables
yesNoQuestionList = ["yes", "no"]
genres = ["happy", "sad", "emotional", "relaxed", "chill", "adventurous",
          "excited", "scary", "actors", "actor, actress", "movies"]
suggestionKeywordList = ["suggest", "recommend", "recommendation"]
whoKeywordList = ["who are you", "who are you?"]
howKeywordList = ["how can you help?", "how can you help", "what can you do"]
whatKeywordList = ["what kind of movies can you recommend?",
                   "what kind of movies can you recommend", "what kind of movies can you recommend to me"]
welcomeKeywordList = ["hi", "hello"]

# Return Prompts
SUGGEST_KEYWORD_PROMPT = "Sure, what genre or actors/actresses are you interested in right now? I'd be happy to provide you with some movie recommendations?"
WHO_KEYWORD_PROMPT = "I am a movie recommender who is always here for you to give movie suggestions at all time."
HOW_KEYWORD_PROMPT = "I can recommend movie based on you prefered genre and I am connected to IMDB so I can provide you the IMDB URL as well."
WHAT_KEYWORD_PROMPT = "I can recommend movie based on genre : happy, sad, emotional, relaxed, chill, adventurous, excited, scary, horror and romantic."
WELCOME_KEYWORD_PROMPT = "Hello! How can I assist you today? Are you in the mood for a movie recommendation?"
MOVIE_NOT_FOUND_PROMPT = "I'm sorry, but I couldn't find any movie recommendations for your mood."
NOT_RELATED_MOVIE_PROMPT = "The query is not related to movie. I am trained to answer any query related to movies."
BASE_PROMPT = "Is the following sentence related to movies, movie genre, mood, or a simple yes or no answer? Sentence:"
