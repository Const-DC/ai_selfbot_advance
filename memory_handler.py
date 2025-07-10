import json
import time
import emoji
import re
import os
from threading import Lock
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.sentiment import SentimentIntensityAnalyzer
from concurrent.futures import ThreadPoolExecutor

# File path for memory
JSON_FILE = "aria_memory.json"

# Thread executor + lock
executor = ThreadPoolExecutor(max_workers=5)
file_lock = Lock()

# NLP components
stop_words = set(stopwords.words("english"))
stemmer = PorterStemmer()
sentiment_analyzer = SentimentIntensityAnalyzer()

def initialize_json_file():
    """Create memory file if missing or corrupted."""
    try:
        with open(JSON_FILE, "r") as f:
            json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        with open(JSON_FILE, "w") as f:
            json.dump([], f)

# Run once on load
initialize_json_file()

def clean_message(message: str):
    if not message:
        return ""
    msg = emoji.replace_emoji(message, replace="")
    msg = re.sub(r"[^\w\s]", "", msg.lower())
    tokens = word_tokenize(msg)
    return " ".join([stemmer.stem(w) for w in tokens if w not in stop_words])

def detect_emotion(message: str):
    if not message:
        return "neutral"
    scores = sentiment_analyzer.polarity_scores(message)
    compound = scores["compound"]
    if compound > 0.5:
        return "happy"
    elif compound < -0.5:
        return "sad"
    else:
        return "neutral"

def save_to_memory(sender: str, message: str):
    if not sender or not message:
        return

    cleaned = clean_message(message)
    if not cleaned:
        return

    emotion = detect_emotion(message)
    memory_entry = {
        "timestamp": time.time(),
        "sender": sender,
        "message": cleaned,
        "emotion": emotion
    }

    def save():
        with file_lock:
            try:
                with open(JSON_FILE, "r") as f:
                    memory = json.load(f)
                memory.append(memory_entry)
                with open(JSON_FILE, "w") as f:
                    json.dump(memory, f, indent=4)
            except Exception as e:
                print(f"❌ Error saving to memory: {e}")

    executor.submit(save)

def get_recent_memory(n=10):
    def fetch():
        with file_lock:
            try:
                with open(JSON_FILE, "r") as f:
                    memory = json.load(f)
                recent = sorted(memory, key=lambda x: x["timestamp"], reverse=True)[:n]
                return recent
            except Exception as e:
                print(f"❌ Error retrieving recent memory: {e}")
                return []

    recent = executor.submit(fetch).result()
    return "\n".join([f"{m['sender']} ({m['emotion']}): {m['message']}" for m in recent])

def get_memory_stats():
    def fetch():
        with file_lock:
            try:
                with open(JSON_FILE, "r") as f:
                    memory = json.load(f)
                timestamps = [m["timestamp"] for m in memory]
                return {
                    "total_entries": len(memory),
                    "oldest_timestamp": min(timestamps) if timestamps else None,
                    "newest_timestamp": max(timestamps) if timestamps else None
                }
            except Exception as e:
                print(f"❌ Error retrieving memory stats: {e}")
                return {
                    "total_entries": 0,
                    "oldest_timestamp": None,
                    "newest_timestamp": None
                }

    return executor.submit(fetch).result()
