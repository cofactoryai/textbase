import textbase
from textbase.message import Message
from textbase import models
import os
from typing import List

# Load your OpenAI API key
models.OpenAI.api_key = "YOUR_API_KEY"
import importlib
# from config import WEATHER_PLUGIN_CONFIG
import config

# Load your OpenAI API key
models.OpenAI.api_key = "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"
# or from environment variable:
# models.OpenAI.api_key = os.getenv("OPENAI_API_KEY")

# Prompt for GPT-3.5 Turbo
SYSTEM_PROMPT = """You are chatting with an AI. There are no specific prefixes for responses, so you can ask or talk about anything you like. The AI will respond in a natural, conversational manner. Feel free to start the conversation with any question or topic, and let's have a pleasant chat!
"""

# Plugin Registry
plugins_registry = {
    "weather": {
        "module": "plugins.weather.plugin",
        "functions": {
            "get_weather": "get_weather",
        },
    },
    "time_and_date": {
        "module": "plugins.time_and_date.plugin",
        "functions": {
            "get_current_time": "get_current_time",
            "get_current_date": "get_current_date",
        },
    },
    "calculator": {
        "module": "plugins.calculator.plugin",
        "functions": {
            "calculate": "calculate",
        },
    },
    "reminder": {
        "module": "plugins.reminder.plugin",
        "functions": {
            "set_reminder": "set_reminder",
            "get_reminders": "get_reminders",
        },
    },
}

@textbase.chatbot("talking-bot")
def on_message(message_history: List[Message], state: dict = None):
    """Your chatbot logic here
    message_history: List of user messages
    state: A dictionary to store any stateful information

    Return a string with the bot_response or a tuple of (bot_response: str, new_state: dict)
    """

    if state is None or "counter" not in state:
        state = {"counter": 0}
    else:
        state["counter"] += 1

    # Set a default value for bot_response
    bot_response = ""

    # # Retrieve the latest user message from message_history
    # user_input = message_history[-1].content
    # Get the latest user message content
    user_input = message_history[-1].content.strip().lower()

    # Check if the user input corresponds to a plugin command
    if user_input.startswith("weather"):
        # Extract the location from the user input (e.g., "weather in New York")
        location = user_input.split("weather")[-1].strip()

        # If no location specified, use the default location from the configuration
        if not location:
            location = config.WEATHER_PLUGIN_CONFIG["default_location"]

        # Check if the weather plugin is available in the registry
        if "weather" in plugins_registry:
            weather_plugin = plugins_registry["weather"]
            module = importlib.import_module(weather_plugin["module"])
            function_name = weather_plugin["functions"]["get_weather"]

            # Call the plugin function and get the response
            bot_response = getattr(module, function_name)(location)
        else:
            bot_response = "Weather plugin is not available."

    elif user_input == "time":
        # Check if the time_and_date plugin is available in the registry
        if "time_and_date" in plugins_registry:
            time_plugin = plugins_registry["time_and_date"]
            module = importlib.import_module(time_plugin["module"])
            function_name = time_plugin["functions"]["get_current_time"]

            # Call the plugin function and get the response
            bot_response = getattr(module, function_name)()
        else:
            bot_response = "Time and Date plugin is not available."

    elif user_input == "date":
        # Check if the time_and_date plugin is available in the registry
        if "time_and_date" in plugins_registry:
            time_plugin = plugins_registry["time_and_date"]
            module = importlib.import_module(time_plugin["module"])
            function_name = time_plugin["functions"]["get_current_date"]

            # Call the plugin function and get the response
            bot_response = getattr(module, function_name)()
        else:
            bot_response = "Time and Date plugin is not available."

    elif user_input.startswith("calculate"):
        # Extract the mathematical expression from the user input
        expression = user_input.split("calculate")[-1].strip()

        # Check if the calculator plugin is available in the registry
        if "calculator" in plugins_registry:
            calculator_plugin = plugins_registry["calculator"]
            module = importlib.import_module(calculator_plugin["module"])
            function_name = calculator_plugin["functions"]["calculate"]

            # Call the plugin function and get the response
            bot_response = getattr(module, function_name)(expression)
        else:
            bot_response = "Calculator plugin is not available."
    
    elif user_input.startswith("set reminder"):
        user_id = config.REMINDER_PLUGIN_CONFIG["default_id"]
        # Extract the task and time from the user input (e.g., "set reminder Call John in 30 minutes")
        parts = user_input.split("set reminder", 1)[-1].strip().split("in", 1)
        task = parts[0].strip()
        time_in_minutes = parts[1].strip()

        # Check if the reminder plugin is available in the registry
        if "reminder" in plugins_registry:
            reminder_plugin = plugins_registry["reminder"]
            module = importlib.import_module(reminder_plugin["module"])
            function_name = reminder_plugin["functions"]["set_reminder"]

            # Call the plugin function and get the response
            bot_response = getattr(module, function_name)(user_id, task, time_in_minutes)
        else:
            bot_response = "Reminder plugin is not available."

    elif user_input == "get reminders":
        user_id = config.REMINDER_PLUGIN_CONFIG["default_id"]
        # Check if the reminder plugin is available in the registry
        if "reminder" in plugins_registry:
            reminder_plugin = plugins_registry["reminder"]
            module = importlib.import_module(reminder_plugin["module"])
            function_name = reminder_plugin["functions"]["get_reminders"]

            # Call the plugin function and get the response
            bot_response = getattr(module, function_name)(user_id)
        else:
            bot_response = "Reminder plugin is not available."

    else:
        # Generate GPT-3.5 Turbo response
        bot_response = models.OpenAI.generate(
            system_prompt=SYSTEM_PROMPT,
            message_history=message_history,
            model="gpt-3.5-turbo",
        )

    return bot_response, state
