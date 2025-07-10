import discord
from discord.ext import commands
import asyncio
import random
import requests
import os
import dotenv
import nltk
import re
import emoji
from persona import bot_persona
from memory_handler import save_to_memory, get_recent_memory
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.sentiment import SentimentIntensityAnalyzer

# Load .env variables
dotenv.load_dotenv()

# Download NLTK resources if missing
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('vader_lexicon', quiet=True)

# Allowed user IDs for interaction
ALLOWED_USER_IDS = [
    #1393442227961263245,
    #123445540691798070,
    #1239177223337017118
]

# NLP tools
stop_words = set(stopwords.words("english"))
stemmer = PorterStemmer()
sentiment_analyzer = SentimentIntensityAnalyzer()

# Selfbot Class
class SelfBot(commands.Bot):
    def __init__(self, model="dolphin-mistral", endpoint="LocalHostHere"): #add your local host link here
        super().__init__(command_prefix="!", self_bot=True)
        self.model = model
        self.endpoint = endpoint

    async def on_ready(self):
        print(f"✅ Logged in as {self.user} ({self.user.id})")

    def clean_message(self, msg):
        msg = emoji.replace_emoji(msg, replace="")
        msg = re.sub(r'[^\w\s]', '', msg.lower())
        tokens = word_tokenize(msg)
        return " ".join([stemmer.stem(word) for word in tokens if word not in stop_words])

    def analyze_user_input(self, msg):
        cleaned = self.clean_message(msg)
        score = sentiment_analyzer.polarity_scores(cleaned)['compound']
        if score > 0.5:
            return "happy"
        elif score < -0.5:
            return "sad"
        elif "?" in msg or "..." in msg:
            return "uncertain"
        else:
            return "neutral"

    def query_ollama(self, user_input):
        try:
            mood = self.analyze_user_input(user_input)
            history = get_recent_memory(n=10)
            prompt = f"""
You are Ava, girl. bratty, flirty, reckless, and never out of character.  

{bot_persona()}

Recent memory: read this always so you can reply like a real person
{history}

User: "{user_input}"

Reply in ONE short sentence, casual, like a real DM. No persona or instructions, just reply, dont add emojies. dont add puntuartion. or any spacial symbols.
"""
            res = requests.post(
                self.endpoint,
                json={"model": self.model, "prompt": prompt, "stream": False}
            )
            raw = res.json().get("response", "")
            lines = [l.strip(' "\n') for l in raw.split("\n") if l.strip()]
            reply = next((l for l in lines if not any(p in l.lower() for p in bot_persona()) and len(l) < 80), None)
            return reply or lines[0] if lines else "uhh idek rn"
        except Exception as e:
            print("Ollama error:", e)
            return "ugh, idk rn"

    async def on_message(self, msg: discord.Message):
        if msg.author.id == self.user.id:
            return

        is_dm = isinstance(msg.channel, discord.DMChannel)
        if not is_dm and msg.author.id not in ALLOWED_USER_IDS and not self.user.mentioned_in(msg):
            return

        try:
            await asyncio.sleep(random.uniform(6, 9))
            async with msg.channel.typing():
                await asyncio.sleep(random.uniform(2, 6))
                reply = self.query_ollama(msg.content)
            await msg.channel.send(reply)
            save_to_memory("you", msg.content)
            save_to_memory("ava", reply)
        except Exception as e:
            print("Failed to send reply:", e)

        await self.process_commands(msg)

# Run
token = os.getenv("DISCORD_BOT_TOKEN")
if not token:
    raise RuntimeError("DISCORD_BOT_TOKEN not set in .env file!")

bot = SelfBot()
bot.run(token)
