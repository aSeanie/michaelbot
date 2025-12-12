import re
import os
import logging
import discord
from discord.ext import commands
from dotenv import load_dotenv
import webserver

# -------------------------
# Load environment variables
# -------------------------
load_dotenv()
token = os.getenv("DISCORD_TOKEN")

# -------------------------
# Logging configuration
# -------------------------
handler = logging.FileHandler(
    filename='discord.log',
    encoding='utf-8',
    mode='w'
)

# -------------------------
# Discord bot setup
# -------------------------
intents = discord.Intents.default()
intents.messages = True
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

# -------------------------
# Message Listener
# -------------------------
@bot.event
async def on_message(message):

    if message.author == bot.user:
        return

    text = message.content.lower()

    # Movies category
    if re.search(r"\b(movie|movies|theatre|theatres)\b", text):
        await message.channel.send("sorry im seeing it with J")

    # Eating category
    elif re.search(r"\b(eat|dinner)\b", text):
        await message.channel.send("Im already having steak tonight")

    # Bottom
    elif re.search(r"\bbottom\b", text):
        await message.channel.send("Johnny is such a bottom")

    # Allow commands to still work
    await bot.process_commands(message)

# -------------------------
# Keep Alive Server
# -------------------------
webserver.keep_alive()

# -------------------------
# Run the bot
# -------------------------
bot.run(token, log_handler=handler, log_level=logging.DEBUG)