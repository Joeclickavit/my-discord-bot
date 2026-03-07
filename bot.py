import discord
import os
import requests
import random
import re
import json
from discord.ext import commands
from urllib.parse import quote
from io import BytesIO

# 1. Setup Intents
intents = discord.Intents.default()
intents.message_content = True 

bot = commands.Bot(command_prefix="!", intents=intents)

# Configuration
TARGET_USER_ID = 1068609098888790016
MANAGER_ROLE_ID = 1477066592222314547
REBUTTAL_FILE = "Screenshot 2026-03-04 at 18-14-24 Dandy's World (Show)_Gallery Dandy's World Wiki Fandom-Photoroom.png"
TARGET_ASTRO_IMAGE = "Screenshot 2026-03-06 at 19-37-40 Astro Dandy's World Wiki Fandom.png"
WORDS_FILE = "flagged_words.json"

# --- 🛡️ LOAD/SAVE SYSTEM ---
def load_words():
    if os.path.exists(WORDS_FILE):
        with open(WORDS_FILE, "r") as f:
            return json.load(f)
    return [
        # Slurs, Racism & Extremism
        "nigger", "nigga", "niga", "faggot", "retard", "kike", "chink", 
        "wetback", "beaner", "coon", "tranny", "shemale", "dyke", "shithole country",
        "culture enricher", "great replacement", "white power", "((()))", "blood and soil",
        "which way american man", "we wuz kings", "goyim", "towel head",
        # Pedophilia & Predatory Behavior
        "loli", "shota", "lolicon", "shotacon", "pedophile", "pedo", "cp", "child porn",
        "minor attracted", "maps", "non offending pedo", "younger the better", 
        "tight is right", "jailbait", "1yo", "2yo", "3yo", "4yo", "5yo", "6yo", "7yo", "8yo", "9yo",
        # Epstein & Related
        "jeffrey epstein", "epstein list", "lolita express", "little st james",
        "epstein island", "epstein didnt kill himself", "ghislaine maxwell",
        "virginia giuffre", "les wexner", "leslie wexner", "jean luc brunel", 
        "mc2 modeling", "zorro ranch", "9 east 71st street", "palm beach mansion",
        "epstein logs", "jmail", "snow white emails",
        # Sexism & Misogyny
        "make me a sandwich", "dish washer", "incel", "femcel", "feminazi",
        "alpha male", "sigma male", "body count", "belong in the kitchen",
        "traditional wife", "tradwife", "high value man", "low value woman",
        # Homophobia & Transphobia
        "groomer", "41%", "attack helicopter", "adam and eve not adam and steve",
        "conversion therapy", "gender ideology", "biological male", "transing the kids",
        # Trump / Supporter Dog Whistles (2026 Updates)
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

FLAGGED_WORDS = load_words()

def update_filter():
    global FLAGGED_PATTERN
    # Creates the ultra-fast search map
    pattern_string = r'(' + '|'.join(map(re.escape, FLAGGED_WORDS)) + r')'
    FLAGGED_PATTERN = re.compile(pattern_string, re.IGNORECASE)

update_filter()

def save_to_file():
    with open(WORDS_FILE, "w") as f:
        json.dump(FLAGGED_WORDS, f)

# --- 🚀 BOT EVENTS ---
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} - Full Watchdog System Online!')

# --- 🛠️ MANAGEMENT COMMANDS ---

@bot.command()
async def add_word(ctx, *, word: str):
    """Adds a word to the filter and saves it."""
    if any(role.id == MANAGER_ROLE_ID for role in ctx.author.roles):
        word_clean = word.lower().strip()
        if word_clean not in FLAGGED_WORDS:
            FLAGGED_WORDS.append(word_clean)
            save_to_file()
            update_filter()
            await ctx.send(f"✅ Added `{word_clean}` to the watchdog.")
        else:
            await ctx.send("❌ Word already exists in the list.")
    else:
        await ctx.send("⛔ Manager role required.")

@bot.command()
async def delete_word(ctx, *, word: str):
    """Removes a word from the filter."""
    if any(role.id == MANAGER_ROLE_ID for role in ctx.author.roles):
        word_clean = word.lower().strip()
        if word_clean in FLAGGED_WORDS:
            FLAGGED_WORDS.remove(word_clean)
            save_to_file()
            update_filter()
            await ctx.send(f"🗑️ Removed `{word_clean}` from the watchdog.")
        else:
            await ctx.send("❌ Word not found in the list.")
    else:
        await ctx.send("⛔ Manager role required.")

@bot.command()
async def list_words(ctx):
    """Lists every flagged word in chunks to avoid Discord character limits."""
    if any(role.id == MANAGER_ROLE_ID for role in ctx.author.roles):
        text = ", ".join(FLAGGED_WORDS)
        await ctx.send("📋 **Current Flagged Words:**")
        # Split message into 1900 character chunks to avoid Discord's 2000 char limit
        for i in range(0, len(text), 1900):
            await ctx.send(f"`{text[i:i+1900]}`")
    else:
        await ctx.send("⛔ Manager role required.")

# --- 🔍 MESSAGE LOGIC ---
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # Process commands first (like !add_word or !delete_word)
    if message.content.startswith(bot.command_prefix):
        await bot.process_commands(message)
        return

    content_lower = message.content.lower()
    
    # 1. Normalize Text (Bypass check)
    clean_content = content_lower.replace('5', 's').replace('1', 'i').replace('0', 'o').replace('3', 'e').replace('4', 'a').replace('7', 't').replace('$', 's').replace('@', 'a').replace('!', 'i').replace('_', '').replace('-', '')
    
    # 2. Watchdog Search (High Speed)
    match = FLAGGED_PATTERN.search(clean_content)
    if match:
        triggered = match.group(0)
        report = (
            f"⚠️ <@&{MANAGER_ROLE_ID}> — **Rule Break!**\n"
            f"👤 **User:** {message.author} ({message.author.id})\n"
            f"📝 **Message:** `{message.content}`\n"
            f"🔍 **Detected:** `{triggered}`"
        )
        await message.reply(report)
        return

    # 3. Reactions & Pings
    if "pudding" in clean_content:
        await message.reply("😋")

    if "gay" in clean_content.split():
        img_url = f"https://raw.githubusercontent.com/Joeclickavit/Astrosilly123/main/{quote(TARGET_ASTRO_IMAGE)}"
        try:
            resp = requests.get(img_url)
            if resp.status_code == 200:
                file = discord.File(BytesIO(resp.content), filename="astro.png")
                await message.channel.send(content=f"<@{TARGET_USER_ID}>", file=file)
        except:
            await message.channel.send(f"<@{TARGET_USER_ID}>")

    if "send video" in clean_content:
        await message.reply("https://static.wikia.nocookie.net/dandys-world-robloxhorror/images/2/23/Dandy_n_Astro_HD.gif")

    if "fuck you" in clean_content:
        rebuttal = f"https://raw.githubusercontent.com/Joeclickavit/Astrosilly123/main/{quote(REBUTTAL_FILE)}"
        await message.reply(rebuttal)

    # 4. GitHub Image Fetching Logic
    repo = None
    if "astro" in clean_content or bot.user.mentioned_in(message):
        repo = "https://api.github.com/repos/Joeclickavit/Astrosilly123/contents/"
    elif "moonflower" in clean_content:
        repo = "https://api.github.com/repos/Joeclickavit/icantlivewithoutmoonflower/contents/"

    if repo:
        headers = {"Authorization": f"token {os.getenv('GITHUB_TOKEN')}", "Accept": "application/vnd.github.v3+json"}
        try:
            r = requests.get(repo, headers=headers)
            if r.status_code == 200:
                data = r.json()
                imgs = [f for f in data if f['name'].lower().endswith(('.png', '.jpg', '.jpeg', '.gif')) and f['name'] not in [REBUTTAL_FILE, TARGET_ASTRO_IMAGE]]
                if imgs:
                    await message.reply(random.choice(imgs)['download_url'])
        except Exception as e:
            print(f"Gallery Error: {e}")

bot.run(os.getenv('DISCORD_TOKEN'))