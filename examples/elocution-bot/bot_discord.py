import os
import openai
import discord
from discord.ext import commands
from gtts import gTTS
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

# Set your Tokens/API Keys here
openai.api_key = ''
DISCORD_TOKEN = ''

# A display message to show that the bot is running
@bot.event
async def on_ready():
    print("Elocution Bot is up and running!")

# An error message for using wrong command format
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Please use the correct syntax: `/pronounce {word}`")
        print("Error! Command not found.")

# Function to handle the /pronounce command
@bot.command()
async def pronounce(ctx, *, word=None):
    print(f"Request arrived from {ctx.author.name} for the word: {word}")
    if word is None:
        await ctx.reply("Please use the correct syntax: `/pronounce {word}`")
        return

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an elocution and pronunciation tutor. Your goal is to help users improve their speech and pronunciation by focusing on syllable sounds."},
                {"role": "user", "content": f"Help me pronounce the word: {word}"}
            ],
            max_tokens=150,
            temperature=0.7
        )
        pronunciation_instructions = response.choices[0].message["content"].strip()
        tts = gTTS(text=pronunciation_instructions, lang='en')
        tts.save(f"{word}.mp3")
        await ctx.reply(f"Here's your pronunciation for: {word}")
        await ctx.reply(file=discord.File(f"{word}.mp3"))
        os.remove(f"{word}.mp3")

    except Exception as e:
        print("Error generating response: ", e)
        await ctx.reply("Error generating response! Please try again.")

bot.run(DISCORD_TOKEN)