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

# The specific filename to exclude from random Astro pool
REBUTTAL_FILE = "Screenshot 2026-03-04 at 18-14-24 Dandy's World (Show)_Gallery Dandy's World Wiki Fandom-Photoroom.png"

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} - Watchdog & Media Mode Active!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    content = message.content.lower()

    # --- 🎥 1. "SEND VIDEO" GIF REACTION ---
    if "send video" in content:
        # We use the direct link to the GIF so Discord plays it automatically
        gif_url = "https://static.wikia.nocookie.net/dandys-world-robloxhorror/images/2/23/Dandy_n_Astro_HD.gif"
        await message.reply(gif_url)
        return

    # --- 🖕 2. CUSTOM "FUCK YOU" REACTION ---
    if "fuck you" in content:
        rebuttal_url = f"https://raw.githubusercontent.com/Joeclickavit/Astrosilly123/main/{quote(REBUTTAL_FILE)}"
        await message.reply(rebuttal_url)
        return 

    # --- 🛡️ 3. WATCHDOG SECTION ---
    FLAGGED_WORDS = [
        "nigger", "nigga", "niga", "faggot", "retard", "kike", "chink", 
        "wetback", "beaner", "coon", "tranny", "shemale", "dyke",
        "kys", "kill yourself", "hope you die", "go hang", 
        "loli", "shota", "lolicon", "shotacon", "pedophile"
    ]

    if any(word in content for word in FLAGGED_WORDS):
        manager_role_id = "1477066592222314547"
        await message.reply(f"⚠️ <@&{manager_role_id}> — This message **possibly broke a rule**. Please review.")

    # --- 📸 4. YOUR ORIGINAL ASTRO IMAGE LOGIC (With Filter) ---
    if "astro" in content or bot.user.mentioned_in(message):
        repo_url = "https://api.github.com/repos/Joeclickavit/Astrosilly123/contents/"
        
        headers = {
            "Authorization": f"token {os.getenv('GITHUB_TOKEN')}",
            "Accept": "application/vnd.github.v3+json"
        }

        try:
            response = requests.get(repo_url, headers=headers)
            
            if response.status_code == 200:
                files = response.json()
                # Filter images and exclude the "fuck you" file
                images = [
                    f for f in files 
                    if f['name'].lower().endswith(('.png', '.jpg', '.jpeg', '.gif')) 
                    and f['name'] != REBUTTAL_FILE
                ]
                
                if images:
                    random_image = random.choice(images)
                    await message.reply(random_image['download_url'])
                else:
                    await message.reply("I found the folder, but there are no silly astros inside! 🌑")
            else:
                await message.reply(f"GitHub connection failed. Check your token!")

        except Exception as e:
            print(f"Error: {e}")
            await message.reply("My brain short-circuited! Check the Railway logs.")

    await bot.process_commands(message)

bot.run(os.getenv('DISCORD_TOKEN'))