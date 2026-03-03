import discord
import os
import requests
import random
from discord.ext import commands

# 1. Setup Intents (Crucial for the bot to "see" messages)
intents = discord.Intents.default()
intents.message_content = True  # Must be ON in Discord Developer Portal
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

# 2. Configuration (Uses your Railway Variables)
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_OWNER = "YourGitHubUsername"  # <-- CHANGE THIS to your GitHub username
REPO_NAME = "Astrosilly123"        # <-- CHANGE THIS to your repo name
FOLDER_PATH = "images"             # <-- The folder where your photos live

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} - Watchdog Mode Active!')

@bot.event
async def on_message(message):
    # Don't let the bot reply to itself
    if message.author == bot.user:
        return

    # Convert message to lowercase to catch "KYS" or "kys"
    content = message.content.lower()

    # --- 🛡️ GROUP A FLAG LIST ---
    # These are the high-priority words we discussed.
    # You can add "pudding" here temporarily to test it safely!
    FLAGGED_WORDS = [
        "nigger", "nigga", "niga", "faggot", "retard", "kike", "chink", 
        "wetback", "beaner", "coon", "tranny", "shemale", "dyke",
        "kys", "kill yourself", "hope you die", "go hang", 
        "loli", "shota", "lolicon", "shotacon", "pedophile"
    ]

    # --- THE SCANNER ---
    if any(word in content for word in FLAGGED_WORDS):
        # This replies directly to the bad message and pings the Manager role
        # Note: Make sure the role name 'MANAGER' is correct in your server
        await message.reply("⚠️ @MANAGER — This message **possibly broke a rule**. Please review.")

    # --- 📸 ASTRO IMAGE COMMAND ---
    if content == "astro":
        url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FOLDER_PATH}"
        headers = {"Authorization": f"token {GITHUB_TOKEN}"}
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            files = response.json()
            # Filters for images only
            images = [f['download_url'] for f in files if f['name'].lower().endswith(('png', 'jpg', 'jpeg', 'gif'))]
            
            if images:
                random_astro = random.choice(images)
                await message.channel.send(random_astro)
            else:
                await message.channel.send("I couldn't find any images in that folder!")
        else:
            await message.channel.send("GitHub connection failed. Check your Token and Repo name!")

    # Process other commands if you add them later
    await bot.process_commands(message)

# Starts the bot using the Token from Railway
bot.run(os.getenv("DISCORD_TOKEN"))