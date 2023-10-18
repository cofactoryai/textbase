from typing import List
from textbase import bot, Message
from textbase.datatypes import Image, Video, Audio, File

@bot()
def on_message(message_history: List[Message], state: dict = None):

    # Mimic user's response
    bot_response = []
    for message in message_history[-1]["content"]:
        match message['data_type']:
            case 'STRING':
                bot_response.append(message['value'])
            case 'IMAGE_URL':
                bot_response.append(Image(message['value']))
            case 'VIDEO_URL':
                bot_response.append(Video(message['value']))
            case 'AUDIO_URL':
                bot_response.append(Audio(message['value']))
            case 'FILE_URL':
                bot_response.append(File(message['value']))

    # message_history[-1]["content"] structure is

    # [
    #     {
    #         "data_type": "STRING",
    #         "value": "<string value>"
    #     }
    # ]

    return {
        "messages": bot_response,
        "state": state
    }
