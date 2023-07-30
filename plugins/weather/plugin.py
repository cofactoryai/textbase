def get_weather(location):
    # Implement code to fetch weather data for the specified location
    # and return a response with weather details
    # Example:
    weather_data = fetch_weather_data(location)
    response = f"The weather in {location} is {weather_data['description']} with a temperature of {weather_data['temperature']}°C."
    return response

def fetch_weather_data(location):
    # Implement code to fetch weather data from a weather API
    # Return weather data as a dictionary, e.g., {"description": "Sunny", "temperature": 25}
    # For simplicity, let's return a static example:
    return {"description": "Sunny", "temperature": 25}
