from textbase import bot, Message
from typing import List

knowledge_base = {
    "weather": "To check the weather, you can use a weather app or website like Weather.com.",
    "recipes": "You can find a variety of recipes on cooking websites and apps such as AllRecipes, Food Network, or Epicurious.",
    "programming": "There are many programming languages to learn, including Python, Java, JavaScript, and more. You can start with online tutorials and courses.",
    "travel": "To plan your travel, you can use websites like TripAdvisor, Expedia, or Google Flights to find flights, hotels, and activities.",
    "health": "For health-related information, it's best to consult with a healthcare professional or visit trusted websites like WebMD for general health tips.",
    "finance": "To manage your finances, consider using budgeting apps like Mint or personal finance software like Quicken.",
    "movies": "You can watch movies on streaming platforms like Netflix, Amazon Prime Video, and Disney+.",
    "books": "You can find a wide range of books at your local library or online bookstores like Amazon and Barnes & Noble.",
    "music": "You can listen to music on music streaming services like Spotify, Apple Music, and YouTube.",
    "food": "If you're looking for restaurants, you can use apps like Yelp or OpenTable to find places to eat.",
    "technology": "Stay up-to-date with the latest tech news by visiting websites like TechCrunch or The Verge.",
    "sports": "For sports updates and scores, you can follow your favorite sports teams on ESPN or use the ESPN app.",
    "gardening": "To get started with gardening, consider reading books like 'The Well-Tempered Garden' by Christopher Lloyd or 'Rodale's Basic Organic Gardening.'",
    "pets": "If you have pets, make sure to provide them with proper care and consult with a veterinarian for their well-being.",
    "cooking": "Improve your cooking skills by watching cooking tutorials on YouTube or taking cooking classes in your area.",
    "history": "Learn about history through documentaries, books, and online resources such as History.com.",
}

@bot()
def on_message(message_history: List[Message], state: dict = None):
    user_message = message_history[-1]["content"][0]["value"].lower()

    if "help with" in user_message:
        return provide_help(user_message)
    elif "list topics" in user_message:
        return list_topics()
    elif "tell me more about" in user_message:
        return provide_details(user_message)
    elif "recommend" in user_message:
        return make_recommendation(user_message)
    else:
        bot_response = "I can provide information on various topics. You can ask for 'help with <topic>', 'list topics', 'tell me more about <topic>', or 'recommend <topic>' to get started."
        return respond(bot_response)

def provide_help(user_message):
    topic = user_message.replace("help with", "").strip()

    if topic in knowledge_base:
        answer = knowledge_base[topic]
        bot_response = f"Here's some information about '{topic}':\n{answer}"
    else:
        bot_response = "I'm sorry, I don't have information on that specific topic."

    return respond(bot_response)

def list_topics():
    topics_list = "\n".join(knowledge_base.keys())
    bot_response = f"Here are the available topics:\n{topics_list}"
    return respond(bot_response)

def provide_details(user_message):
    topic = user_message.replace("tell me more about", "").strip()

    if topic in knowledge_base:
        answer = knowledge_base[topic]
        bot_response = f"Here's more information about '{topic}':\n{answer}"
    else:
        bot_response = "I'm sorry, I don't have additional information on that specific topic."

    return respond(bot_response)

def make_recommendation(user_message):
    topic = user_message.replace("recommend", "").strip()

    if topic == "movie":
        recommendation = "I recommend checking out the latest movie releases on Netflix."
    elif topic == "book":
        recommendation = "I recommend reading 'The Catcher in the Rye' by J.D. Salinger."
    elif topic == "music":
        recommendation = "I recommend listening to 'Abbey Road' by The Beatles."
    else:
        recommendation = "I'm sorry, I don't have a specific recommendation for that topic."

    return respond(recommendation)

def respond(bot_response):
    response = {
        "data": {
            "messages": [
                {
                    "data_type": "STRING",
                    "value": bot_response
                }
            ],
            "state": None
        },
        "errors": []
    }

    return {
        "status_code": 200,
        "response": response
    }
