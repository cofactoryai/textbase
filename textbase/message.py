@bot()
def on_message(message_history: List[Message], state: dict = None):
    # Extract the latest user message
    user_message = message_history[-1].content[0].value.strip()

    # Check if the user has provided property requirements
    if "budget" in user_message.lower() or "location" in user_message.lower() or "investment goals" in user_message.lower():
        # User has started providing requirements
        bot_response = "Great! Thanks for sharing your preferences. Let's continue. Do you have a specific location in mind, or should I suggest some popular ones?"
    else:
        # User hasn't provided requirements yet, so prompt them
        bot_response = "To assist you better, please share your property requirements. You can start by telling me about your budget, preferred location, and investment goals."

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
