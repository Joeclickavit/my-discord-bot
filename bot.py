import discord
from discord.ext import commands
import requests
import random
import os

# 1. Setup Permissions (Intents)
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# 2. Your Image Repo Link
GITHUB_API_URL = "https://api.github.com/repos/Joeclickavit/Astrosilly123/contents/"

def get_random_astro_image():
    try:
        # Request the list of files from your GitHub repo
        response = requests.get(GITHUB_API_URL)
        if response.status_code == 200:
            # Filter the list for only PNG files
            all_files = response.json()
            png_urls = [file['download_url'] for file in all_files if file['name'].lower().endswith('.png')]
            
            if png_urls:
                return random.choice(png_urls)
    except Exception as e:
        print(f"Error fetching from GitHub: {e}")
    return None

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} - Astro Bot is Ready!')

@bot.event
async def on_message(message):
    # Ignore the bot's own messages
    if message.author == bot.user:
        return

    # Trigger: If "astro" is in the message OR the bot is mentioned
    content = message.content.lower()
    if "astro" in content or bot.user.mentioned_in(message):
        image_url = get_random_astro_image()
        if image_url:
            await message.reply(image_url)
        else:
            await message.reply("I couldn't find any silly Astros right now!")

    await bot.process_commands(message)

# 3. Secure Token Loading
bot.run(os.getenv('DISCORD_TOKEN'))