import discord
import os
import requests
import random
from discord.ext import commands

# 1. Setup Intents
intents = discord.Intents.default()
intents.message_content = True 
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} - Watchdog & Astro Mode Active!')

@bot.event
async def on_message(message):
    # Don't let the bot reply to itself
    if message.author == bot.user:
        return

    content = message.content.lower()

    # --- 🛡️ WATCHDOG SECTION (Group A Flags) ---
    FLAGGED_WORDS = [
        "pudding",  # TEST WORD
        "nigger", "nigga", "niga", "faggot", "retard", "kike", "chink", 
        "wetback", "beaner", "coon", "tranny", "shemale", "dyke",
        "kys", "kill yourself", "hope you die", "go hang", 
        "loli", "shota", "lolicon", "shotacon", "pedophile"
    ]

    if any(word in content for word in FLAGGED_WORDS):
        # Replies and pings the Manager role
        await message.reply("⚠️ @MANAGER — This message **possibly broke a rule**. Please review.")

    # --- 📸 ASTRO IMAGE SECTION ---
    if "astro" in content or bot.user.mentioned_in(message):
        
        # CORRECTED URL for your repo: Joeclickavit/my-discord-bot
        repo_url = "https://api.github.com/repos/Joeclickavit/my-discord-bot/contents/"
        
        headers = {
            "Authorization": f"token {os.getenv('GITHUB_TOKEN')}",
            "Accept": "application/vnd.github.v3+json"
        }

        try:
            response = requests.get(repo_url, headers=headers)
            
            if response.status_code == 200:
                files = response.json()
                # Filter for image files sitting in the main folder
                images = [f for f in files if f['name'].lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
                
                if images:
                    random_image = random.choice(images)
                    await message.reply(random_image['download_url'])
                else:
                    await message.reply("I looked in your repo, but I don't see any image files! 🌑")
            else:
                await message.reply(f"GitHub connection failed (Error {response.status_code}). Check your GITHUB_TOKEN in Railway!")

        except Exception as e:
            print(f"Error fetching images: {e}")
            await message.reply("My brain short-circuited! Check the Railway logs.")

    await bot.process_commands(message)

# Starts the bot using the Token from Railway
bot.run(os.getenv('DISCORD_TOKEN'))