---
sidebar_position: 4
---

# Elocution Bot

This bot makes an API call to OpenAI and helps users learn proper elocution and pronunciation for different words. It uses GPT-3.5 Turbo.

## Textbase Bot
- This bot is the same as Open AI bot except with an updated prompt focusing on elocution and pronunciation of words.
- Please set the Open AI API Key in the `main.py` file inside the `elocution-bot` folder.
- The following prompt has been used for this bot:
```text
SYSTEM_PROMPT = """You are an elocution and pronunciation tutor. Your goal is to help users improve their speech and pronunciation by focusing on syllable sounds.
Please provide clear explanations and examples to help users understand and practice the correct pronunciation of words with different syllable structures.
Also encourage users to ask questions and engage in pronunciation exercises with you.
"""
```

## Discord Bot
- This bot provides the above functionality as a discord bot with audio cues to help the user understand the correct pronunciation.

### Setup Instructions
- Please set the Open AI API Key in the `bot_discord.py` file inside the `elocution-bot` folder.
- To setup this bot go to [Discord Developer Portal](https://discord.com/developers/applications).
- Click on `New Application`, fill in the details and then click on `Create`.
- Feel free to customize your bot as per your liking.
- On the left sidebar, click on `Bot`, then `Reset Token`, copy it and set it as the `DISCORD_TOKEN` in `bot_discord.py` file.
- Turn all three options ON under `Privileged Gateway Inputs`.
- Again on the left sidebar, click on `OAuth2`, set `Authorization Method` to `In-App Authorization`, set `Scopes` to `bot` and turn on the following permissions:
```text
Read Messages/View Channel
Send Messages
Attach Files
Read Message History
Mention everyone
```
- On the left sidebar, click on `URL Generator`, set `Scopes` to `bot`, and turn on the same permissions as above.
- Copy the `Generated URL`, paste it in a browser and add the bot to your required Server.

### Usage Instructions
- To start the bot, run the following command inside `elocution-bot` folder.
```bash
python bot_discord.py
```
- Use the following command (without the braces) to get a response from the bot on any channel in your Discord Server.
```text
/pronounce {word}
```