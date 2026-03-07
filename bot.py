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

# Target User ID to ping
TARGET_USER_ID = 1068609098888790016

# Filenames and Repo info
REBUTTAL_FILE = "Screenshot 2026-03-04 at 18-14-24 Dandy's World (Show)_Gallery Dandy's World Wiki Fandom-Photoroom.png"
GAY_FLOWER_REPO = "Joeclickavit/GayFlower"
GAY_FLOWER_FILE = "Screenshot 2026-03-06 at 19-37-40 Astro Dandy's World Wiki Fandom.png"

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} - GayFlower Ping Active!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    content = message.content.lower()
    
    # --- 🛠️ 1. NORMALIZE TEXT ---
    clean_content = content.replace('5', 's').replace('1', 'i').replace('0', 'o').replace('3', 'e').replace('4', 'a').replace('7', 't').replace('$', 's').replace('@', 'a').replace('!', 'i').replace('_', '').replace('-', '')
    words_in_message = clean_content.split()

    # --- 🌈 2. GAY TRIGGER (Fixed to work like Astro) ---
    if "gay" in words_in_message:
        # We fetch the specific file data via API to get a valid 'download_url'
        repo_url = f"https://api.github.com/repos/{GAY_FLOWER_REPO}/contents/{quote(GAY_FLOWER_FILE)}"
        headers = {"Authorization": f"token {os.getenv('GITHUB_TOKEN')}", "Accept": "application/vnd.github.v3+json"}
        
        try:
            response = requests.get(repo_url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                # Use the download_url which includes the necessary access token for private repos
                image_url = data['download_url']
                await message.channel.send(f"<@{TARGET_USER_ID}> {image_url}")
        except Exception as e:
            print(f"Error fetching GayFlower image: {e}")

    # --- 🍮 3. PUDDING REACTION ---
    if "pudding" in clean_content:
        await message.reply("😋")
    
    # --- 🎥 4. "SEND VIDEO" GIF REACTION ---
    if "send video" in clean_content:
        gif_url = "https://static.wikia.nocookie.net/dandys-world-robloxhorror/images/2/23/Dandy_n_Astro_HD.gif"
        await message.reply(gif_url)

    # --- 🖕 5. CUSTOM "FUCK YOU" REACTION ---
    if "fuck you" in clean_content:
        rebuttal_url = f"https://raw.githubusercontent.com/Joeclickavit/Astrosilly123/main/{quote(REBUTTAL_FILE)}"
        await message.reply(rebuttal_url)

    # --- 🛡️ 6. SMART WATCHDOG LIST ---
    FLAGGED_WORDS = [
        "nigger", "nigga", "niga", "faggot", "retard", "kike", "chink", 
        "wetback", "beaner", "coon", "tranny", "shemale", "dyke", "shithole country",
        "culture enricher", "great replacement", "white power", "((()))", "blood and soil",
        "which way american man", "we wuz kings", "goyim", "towel head",
        "loli", "shota", "lolicon", "shotacon", "pedophile", "pedo", "cp", "child porn",
        "minor attracted", "maps", "non offending pedo", "younger the better", 
        "tight is right", "jailbait", "1yo", "2yo", "3yo", "4yo", "5yo", "6yo", "7yo", "8yo", "9yo",
        "jeffrey epstein", "epstein list", "lolita express", "little st james",
        "epstein island", "epstein didnt kill himself", "ghislaine maxwell",
        "virginia giuffre", "les wexner", "leslie wexner", "jean luc brunel", 
        "mc2 modeling", "zorro ranch", "9 east 71st street", "palm beach mansion",
        "epstein logs", "jmail", "snow white emails",
        "make me a sandwich", "dish washer", "incel", "femcel", "feminazi",
        "alpha male", "sigma male", "body count", "belong in the kitchen",
        "traditional wife", "tradwife", "high value man", "low value woman",
        "groomer", "41%", "attack helicopter", "adam and eve not adam and steve",
        "conversion therapy", "gender ideology", "biological male", "transing the kids",
        "maga", "ultra maga", "trump 2024", "trump 2026", "trump 2028", "trump train",
        "make america great again", "keep america great", "kag", "america first",
        "drain the swamp", "fake news", "witch hunt", "stop the steal", "lock her up",
        "truth social", "don junior", "vance 2028", "golden age of america", 
        "americas revival", "save america", "47th president", "drill baby drill", 
        "rino", "crooked joe", "laffin kamala", "project 2025", "border czar",
        "charlie kirk", "one homeland", "one people", "one heritage", "dei hire",
        "illegal alien", "invasion at the border", "mass deportation", "deport them all",
        "build the wall", "finish the wall", "freedom 250", "dalilah law", "angel moms"
    ]

    is_bad = False
    triggered_word = ""
    for flagged in FLAGGED_WORDS:
        if " " in flagged:
            if flagged in clean_content:
                is_bad = True
                triggered_word = flagged
                break
        else:
            if flagged in words_in_message:
                is_bad = True
                triggered_word = flagged
                break

    if is_bad:
        manager_role_id = "1477066592222314547"
        log_report = (
            f"⚠️ <@&{manager_role_id}> — **Rule Break Detected!**\n"
            f"👤 **User:** {message.author} ({message.author.id})\n"
            f"📝 **Original Message:** `{message.content}`\n"
            f"🔍 **Detected As:** `{triggered_word}`"
        )
        await message.reply(log_report)

    # --- 📸 7. ORIGINAL ASTRO IMAGE LOGIC ---
    if not is_bad:
        if "astro" in clean_content or bot.user.mentioned_in(message):
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
                print(f"Error fetching images: {e}")

    await bot.process_commands(message)

bot.run(os.getenv('DISCORD_TOKEN'))