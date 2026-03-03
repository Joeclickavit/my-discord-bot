import discord
import os
import requests
import random
from discord.ext import commands

# 1. Setup Intents (This fixes the 'PrivilegedIntents' error you had)
intents = discord.Intents.default()
intents.message_content = True 

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} - Ready!')

@bot.event
async def on_message(message):
    # Don't let the bot reply to itself
    if message.author == bot.user:
        return

    # Trigger words: "astro" or mentioning the bot
    if "astro" in message.content.lower() or bot.user.mentioned_in(message):
        
        # GitHub API settings
        repo_url = "https://api.github.com/repos/Joeclickavit/Astrosilly123/contents/"
        
        # 2. Use your GITHUB_TOKEN to avoid the 60-minute limit
        headers = {
            "Authorization": f"token {os.getenv('GITHUB_TOKEN')}",
            "Accept": "application/vnd.github.v3+json"
        }

        try:
            response = requests.get(repo_url, headers=headers)
            
            if response.status_code == 200:
                files = response.json()
                # Filter for image files only
                images = [f for f in files if f['name'].lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
                
                if images:
                    random_image = random.choice(images)
                    # Send the download URL so Discord shows the image preview
                    await message.reply(random_image['download_url'])
                else:
                    await message.reply("I found the folder, but there are no silly astros inside! 🌑")
            else:
                await message.reply(f"GitHub is grumpy right now (Error {response.status_code}). Try again in a bit!")

        except Exception as e:
            print(f"Error fetching images: {e}")
            await message.reply("My brain short-circuited trying to find an astro. Check the Railway logs!")

    await bot.process_commands(message)

# 3. Get the token from Railway's Variables
bot.run(os.getenv('DISCORD_TOKEN'))