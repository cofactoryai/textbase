import textbase

# Initialize the TextBase chatbot UI
chatbot = textbase.Chatbot()

# Function to get movie recommendations
def get_movie_recommendations(parameters):
    # You can implement your recommendation logic here based on user preferences.
    recommendations = ["Inception", "The Shawshank Redemption", "Interstellar", "Avatar"]
    return recommendations

# Function to get movie details
def get_movie_details(parameters):
    movie_name = parameters.get("movie_name")
    # You can implement logic to fetch movie details from a database or API here.
    # For simplicity, we'll just return a sample response.
    movie_details = f"Details for {movie_name}: Director - Christopher Nolan, Year - 2010"
    return movie_details

# Define chatbot functions
chatbot.register_function("get_movie_recommendations", get_movie_recommendations)
chatbot.register_function("get_movie_details", get_movie_details)

# Start the chatbot conversation loop
while True:
    user_input = chatbot.get_user_input()
    response = chatbot.generate_response(user_input)
    chatbot.send_message(response)
