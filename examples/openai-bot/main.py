from textbase import bot, Message
from textbase.models import OpenAI
from typing import List
import pandas as pd
import pandas as pd
# Load your OpenAI API key
OpenAI.api_key = "YOUR_API_KEY_HERE"  # Replace with your actual API key

# Load property data from a CSV file
property_data = pd.read_csv("property_data.csv")  # Replace with the actual CSV file path

# Prompt for GPT-3.5 Turbo
SYSTEM_PROMPT = """Welcome to the Best Property Finder! 

I'm here to assist you in finding the perfect property investment that aligns with your unique preferences and behavior.
To do that, let's engage in a meaningful conversation:    
Tell me about your financial situation. What's your budget or investment capacity? Feel free to share your goals.
Describe your ideal location for property investment. What city or neighborhood attracts you, and why?
What are your long-term and short-term investment goals? How do you envision profiting from this investment?
Imagine your dream property. What type of property appeals to you the most? What features or amenities are essential?
Are you looking to diversify your investment portfolio or focusing solely on real estate?
Share your thoughts on risk. How comfortable are you with investment risks?
Are you willing to take risks for potentially higher returns?
"""

@bot()
def on_message(message_history: List[Message], state: dict = None):
    # Extract the latest user message
    user_message = message_history[-1].content[0].value.strip()

    # Check if the user has provided budget and location
    if "budget" in user_message.lower() and "location" in user_message.lower():
        # User has provided budget and location, perform property search
        budget = extract_budget(user_message)  # Implement a function to extract budget from user input
        location = extract_location(user_message)  # Implement a function to extract location from user input

        # Perform property search based on budget and location
        property_results = search_properties(budget, location)  # Implement the property search function

        if property_results:
            bot_response = "Here are some properties that match your criteria:\n\n"
            for result in property_results:
                bot_response += f"- {result['property_name']} in {result['location']} for ${result['price']}\n"

        else:
            bot_response = "I couldn't find any properties that match your criteria. Please try different budget or location."

    else:
        # User hasn't provided budget and location, continue with the standard chatbot responses
        bot_response = OpenAI.generate(
            system_prompt=SYSTEM_PROMPT,
            message_history=message_history,
            model="gpt-3.5-turbo",
        )

    response = {
        "data": {
            "messages": [
                {
                    "data_type": "STRING",
                    "value": bot_response
                }
            ],
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



# Load property data from a CSV file (make sure to adjust the file path)
property_data = pd.read_csv("property_data.csv")

def extract_budget(user_input):
    # Extract budget information from user input using regular expressions
    # For example, extract any numeric value that represents the budget
    matches = re.findall(r'\b\d+\b', user_input)
    if matches:
        return int(matches[0])  # Assuming the first numeric value represents the budget
    return None

def extract_location(user_input):
    # Extract location information from user input using keyword matching
    # You can customize this function to match specific keywords or use more advanced NLP techniques
    keywords = ['location', 'city', 'neighborhood', 'area', 'place']
    for keyword in keywords:
        if keyword in user_input.lower():
            # Remove the keyword from the user input to get the location
            location = user_input.lower().replace(keyword, '').strip()
            return location
    return None

def search_properties(budget, location):
    # Filter the property_data DataFrame based on budget and location
    filtered_properties = property_data

    if budget is not None:
        filtered_properties = filtered_properties[filtered_properties['price'] <= budget]

    if location is not None:
        filtered_properties = filtered_properties[filtered_properties['location'].str.lower() == location.lower()]

    # Convert the filtered results to a list of dictionaries for response
    results = []
    for index, row in filtered_properties.iterrows():
        result = {
            'property_name': row['property_name'],
            'location': row['location'],
            'property_type': row['property_type'],
            'price': row['price']
        }
        results.append(result)

    return results
