import discord
import os
import requests
import random
from discord.ext import commands
from urllib.parse import quote

# 1. Setup Intents
intents = discord.Intents.default()
intents.message_content = True 

bot = commands.Bot(command_prefix="!", intents=intents)

# Filename to exclude from random Astro pool
REBUTTAL_FILE = "Screenshot 2026-03-04 at 18-14-24 Dandy's World (Show)_Gallery Dandy's World Wiki Fandom-Photoroom.png"

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} - Ready for Pudding!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    content = message.content.lower()

    # --- 🍮 1. PUDDING REACTION ---
    if "pudding" in content:
        await message.reply("😋")
        # We don't use 'return' here in case the message also says 'astro'
    
    # --- 🎥 2. "SEND VIDEO" GIF REACTION ---
    if "send video" in content:
        gif_url = "https://static.wikia.nocookie.net/dandys-world-robloxhorror/images/2/23/Dandy_n_Astro_HD.gif"
        await message.reply(gif_url)
        return

    # --- 🖕 3. CUSTOM "FUCK YOU" REACTION ---
    if "fuck you" in content:
        rebuttal_url = f"https://raw.githubusercontent.com/Joeclickavit/Astrosilly123/main/{quote(REBUTTAL_FILE)}"
        await message.reply(rebuttal_url)
        return 

    # --- 🛡️ 4. WATCHDOG SECTION ---
    FLAGGED_WORDS = [
        "nigger", "nigga", "niga", "faggot", "retard", "kike", "chink", 
        "wetback", "beaner", "coon", "tranny", "shemale", "dyke",
        "kys", "kill yourself", "hope you die", "go hang", 
        "loli", "shota", "lolicon", "shotacon", "pedophile"
    ]

    if any(word in content for word in FLAGGED_WORDS):
        manager_role_id = "1477066592222314547"
        await message.reply(f"⚠️ <@&{manager_role_id}> — This message **possibly broke a rule**. Please review.")

    # --- 📸 5. YOUR ORIGINAL ASTRO IMAGE LOGIC ---
    if "astro" in content or bot.user.mentioned_in(message):
        repo_url = "https://api.github.com/repos/Joeclickavit/Astrosilly123/contents/"
        headers = {"Authorization": f"token {os.getenv('GITHUB_TOKEN')}", "Accept": "application/vnd.github.v3+json"}
        try:
            response = requests.get(repo_url, headers=headers)
            if response.status_code == 200:
                files = response.json()
                images = [f for f in files if f['name'].lower().endswith(('.png', '.jpg', '.jpeg', '.gif')) and f['name'] != REBUTTAL_FILE]
                if images:
                    random_image = random.choice(images)
                    await message.reply(random_image['download_url'])
        except Exception as e:
            print(f"Error: {e}")

    await bot.process_commands(message)

bot.run(os.getenv('DISCORD_TOKEN'))