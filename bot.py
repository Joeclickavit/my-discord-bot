import discord
import os
import requests
import random
from discord.ext import commands

# 1. Setup Intents
intents = discord.Intents.default()
intents.message_content = True 

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} - Watchdog Mode Active!')

@bot.event
async def on_message(message):
    # Don't let the bot reply to itself
    if message.author == bot.user:
        return

    # Convert message to lowercase for scanning
    content = message.content.lower()

    # --- 🛡️ WATCHDOG SECTION (Group A Flags) ---
    # 'pudding' has been removed.
    FLAGGED_WORDS = [
        "nigger", "nigga", "niga", "faggot", "retard", "kike", "chink", 
        "wetback", "beaner", "coon", "tranny", "shemale", "dyke",
        "kys", "kill yourself", "hope you die", "go hang", 
        "loli", "shota", "lolicon", "shotacon", "pedophile"
    ]

    if any(word in content for word in FLAGGED_WORDS):
        # Uses your specific Role ID to ping the Manager
        manager_role_id = "1477066592222314547"
        await message.reply(f"⚠️ <@&{manager_role_id}> — This message **possibly broke a rule**. Please review.")

    # --- 📸 YOUR ORIGINAL ASTRO IMAGE LOGIC ---
    if "astro" in content or bot.user.mentioned_in(message):
        
        # Keeping your URL exactly as you requested
        repo_url = "https://api.github.com/repos/Joeclickavit/Astrosilly123/contents/"
        
        headers = {
            "Authorization": f"token {os.getenv('GITHUB_TOKEN')}",
            "Accept": "application/vnd.github.v3+json"
        }

        try:
            response = requests.get(repo_url, headers=headers)
            
            if response.status_code == 200:
                files = response.json()
                images = [f for f in files if f['name'].lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
                
                if images:
                    random_image = random.choice(images)
                    await message.reply(random_image['download_url'])
                else:
                    await message.reply("I found the folder, but there are no silly astros inside! 🌑")
            else:
                await message.reply(f"GitHub is grumpy right now (Error {response.status_code}). Try again in a bit!")

        except Exception as e:
            print(f"Error fetching images: {e}")
            await message.reply("My brain short-circuited trying to find an astro. Check the Railway logs!")

    await bot.process_commands(message)

# Starts the bot using your Railway Token
bot.run(os.getenv('DISCORD_TOKEN'))