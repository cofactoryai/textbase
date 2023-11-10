import os
from configparser import ConfigParser

from telegram.ext import Updater, CommandHandler, MessageHandler, ConversationHandler, Filters
from textbase import bot, Message
from textbase.models import OpenAI
from typing import List
import whisper


class TextBase:
    def __init__(self):
        os.environ["PATH"] = os.path.join(os.path.dirname(__file__),"utils")
        config = ConfigParser()
        config.read(f'utils/config.ini')
        self.token = config.get('TELEGRAM', 'auth_token')
        self.OPENAIKEY = config.get('OPENAI', 'api_key')
        self.PROMT = ""
        self.SELECT_DATA = 1
        self.user_data = {}
        self.model = whisper.load_model("medium")
        self.updater = Updater(self.token, use_context=True)
        self.dispatcher = self.updater.dispatcher
        self.message_handler = None

    def run_bot(self):
        print("Started bot...")
        self.dispatcher.add_handler(CommandHandler('start', self.start))
        self.dispatcher.add_handler(CommandHandler('quit', self.quit))
        self.updater.start_polling()
        self.updater.idle()



    def start(self, update, context):
        update.message.reply_text("Welcome to textbase bot! Send me any message, and I'll respond.")
        self.message_handler = MessageHandler(Filters.all, self.select_data)
        self.dispatcher.add_handler(self.message_handler)


    def quit(self, update, context):
        update.message.reply_text("Goodbye!")
        if self.message_handler:
            self.dispatcher.remove_handler(self.message_handler)
            self.message_handler = None



    def select_data(self, update, context):
        user_id = update.message.chat_id
        self.user_data[user_id] = {'text': None, 'audio': None}
        if update.message.text:
            update.message.reply_text("Text received. Your result is being Prepared")
            self.user_data[user_id]['text'] = update.message.text
        elif update.message.audio or update.message.voice:
            update.message.reply_text("Audio received. Your result is being Prepared")
            audio_file = update.message.audio or update.message.voice
            file_id = audio_file.file_id
            file_path = os.path.join(os.path.dirname(__file__),"audio", f"{user_id}_{file_id}.ogg")
            audio_file.get_file().download(file_path)
            self.user_data[user_id]['audio'] = file_path
            self.generate_text_from_audio(update, context, user_id)
        else:
            update.message.reply_text("No valid data received. Please send either text or an OGG audio file.")
        if self.user_data[user_id]['text']:
            self.PROMT = self.user_data[user_id]['text']
            result = self.on_message([])
            update.message.reply_text(result)

    def generate_text_from_audio(self, update, context, user_id):
        file_path = self.user_data[user_id]['audio']
        result = self.model.transcribe(file_path)["text"]
        self.user_data[user_id]['text'] = result
        update.message.reply_text(f"""
Transcribed Text:
{result}
""")
        os.remove(file_path)


    def on_message(self, message_history: List[Message], state: dict = None ):
        # Generate GPT-3.5 Turbo response
        OpenAI.api_key = self.OPENAIKEY
        bot_response = OpenAI.generate(
            system_prompt=self.PROMT,
            message_history=message_history,  # Assuming history is the list of user messages
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
        response = response["data"]["messages"]
        completeData = ""
        for data in response:
            completeData += data["value"]
        return completeData


if __name__ == '__main__':
    bot = TextBase()
    bot.run_bot()