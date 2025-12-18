import re
import os
import string
import logging
import discord
from discord.ext import commands
from dotenv import load_dotenv
from threading import Thread
import time
import requests
from flask import Flask

# -------------------------
# Load environment variables
# -------------------------
load_dotenv()
token = os.getenv("DISCORD_TOKEN")
public_url = os.getenv("PUBLIC_URL")  # URL of your Render or Replit service

# -------------------------
# Logging configuration
# -------------------------
logging.basicConfig(
    level=logging.DEBUG,
    handlers=[
        logging.FileHandler(filename='discord.log', encoding='utf-8', mode='a'),
        logging.StreamHandler()
    ],
    format="%(asctime)s [%(levelname)s] %(message)s"
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
# Define triggers and responses
# -------------------------
TRIGGERS = {
    r"\b(movie|movies|theatre|theatres)\b": "Im seeing it with J",
    r"\b(eat|dinner|kelseys|chucks)\b": "Im already having steak tonight",
    r"\bbottom\b": "Johnny is such a bottom"
}

# -------------------------
# Helper function: clean text
# -------------------------
def clean_text(text: str) -> str:
    return text.lower().translate(str.maketrans('', '', string.punctuation))

# -------------------------
# Message listener
# -------------------------
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    text = clean_text(message.content)

    for pattern, reply in TRIGGERS.items():
        if re.search(pattern, text):
            await message.channel.send(reply)
            break

    await bot.process_commands(message)

# -------------------------
# Flask web server
# -------------------------
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!"

def run_server():
    app.run(host='0.0.0.0', port=8080)

def ping_self():
    if not public_url:
        logging.warning("PUBLIC_URL not set. Keep-alive pings disabled.")
        return

    logging.info(f"[KEEP-ALIVE] Pinging {public_url} every 4.5 minutes.")

    while True:
        try:
            response = requests.get(public_url, timeout=10)
            logging.debug(f"[KEEP-ALIVE] Ping status: {response.status_code}")
        except requests.RequestException as e:
            logging.warning(f"[KEEP-ALIVE ERROR] {e}")
        time.sleep(280)  # Ping every ~4.5 minutes

def keep_alive():
    # Start Flask server thread
    t = Thread(target=run_server)
    t.daemon = True
    t.start()

    # Start ping thread
    p = Thread(target=ping_self)
    p.daemon = True
    p.start()

# -------------------------
# Start keep-alive threads
# -------------------------
keep_alive()

# -------------------------
# Run the bot
# -------------------------
bot.run(token)

