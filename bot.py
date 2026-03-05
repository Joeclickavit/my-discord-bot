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
    print(f'Logged in as {bot.user} - Watchdog Max Active!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # --- 🛠️ 1. ADVANCED NORMALIZE TEXT ---
    # This catches 1337speak (v4nc3 -> vance, tr0mp -> tromp)
    raw_content = message.content.lower()
    trans_table = str.maketrans('510347$@!', 'siotea sai')
    clean_content = raw_content.translate(trans_table).replace('_', '').replace('-', '')
    words_in_message = clean_content.split()

    # --- 🍮 2. REACTIONS ---
    if "pudding" in clean_content:
        await message.reply("😋")
    if "send video" in clean_content:
        await message.reply("https://static.wikia.nocookie.net/dandys-world-robloxhorror/images/2/23/Dandy_n_Astro_HD.gif")
    if "fuck you" in clean_content:
        await message.reply(f"https://raw.githubusercontent.com/Joeclickavit/Astrosilly123/main/{quote(REBUTTAL_FILE)}")

    # --- 🛡️ 3. MEGA WATCHDOG LIST (~200 PHRASES) ---
    FLAGGED_WORDS = [
        # SLURS & RACISM
        "nigger", "nigga", "niga", "faggot", "retard", "kike", "chink", "wetback", "beaner", "coon", "tranny", "shemale", "dyke", 
        "shithole country", "culture enricher", "great replacement", "white power", "blood and soil", "goyim", "towel head", 
        "border hopper", "spic", "jungle bunny", "porch monkey", "cracker", "paki", "gypsy", "wop", "polack",

        # PEDOPHILIA & PREDATORY (Grooming / CP / MAP)
        "loli", "shota", "lolicon", "shotacon", "pedophile", "pedo", "cp", "child porn", "minor attracted", "maps", 
        "non offending pedo", "younger the better", "jailbait", "age is just a number", "child lover", "barely legal",
        "1yo", "2yo", "3yo", "4yo", "5yo", "6yo", "7yo", "8yo", "9yo", "10yo", "11yo", "12yo", "13yo", "14yo",

        # EPSTEIN & EXPLOITATION
        "jeffrey epstein", "epstein list", "lolita express", "little st james", "epstein island", "ghislaine maxwell",
        "epstein didnt kill himself", "mossad agent", "pedophile island",

        # SEXISM & MISOGYNY
        "make me a sandwich", "dish washer", "incel", "femcel", "feminazi", "alpha male", "sigma male", "body count", 
        "belong in the kitchen", "tradwife", "traditional wife", "high value man", "low value woman", "stay in your lane woman",
        "women are property", "men are superior", "get back to the kitchen", "femitard", "misandry", "misogyny",

        # HOMOPHOBIA & TRANSPHOBIA
        "groomer", "41%", "attack helicopter", "adam and eve not adam and steve", "conversion therapy", "gender ideology", 
        "biological male", "transing the kids", "there are only 2 genders", "mentally ill trans", "lgbtq agenda",

        # TRUMP & 2026 SUPPORTER PHRASES (Filtered for slogans/dog-whistles)
        "maga", "ultra maga", "trump 2024", "trump 2026", "trump 2028", "trump train", "make america great again", 
        "keep america great", "kag", "america first", "drain the swamp", "fake news", "witch hunt", "stop the steal", 
        "lock her up", "truth social", "don junior", "vance 2028", "golden age of america", "americas revival", "save america", 
        "47th president", "drill baby drill", "rino", "crooked joe", "laffin kamala", "project 2025", "border czar", 
        "charlie kirk", "one homeland", "one people", "one heritage", "which way american man", "illegal alien", 
        "invasion at the border", "mass deportation", "deport them all", "build the wall", "finish the wall", 
        "freedom 250", "dalilah law", "angel moms", "refounding father", "american century", "make america glorious again",
        "magaga", "jd vance", "homan for border", "trump dynasty", "dei hire", "woke mind virus", "own the libs",
        "liberal tears", "globalist puppet", "soros funded", "stolen election", "jan 6 patriots", "pardon the patriots",

        # SELF-HARM & VIOLENCE
        "kys", "kill yourself", "hope you die", "go hang", "drink bleach", "commit suicide", "tie a noose"
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

    # --- 📸 4. ORIGINAL ASTRO IMAGE LOGIC ---
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