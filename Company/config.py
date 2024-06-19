import os

from dotenv import load_dotenv

load_dotenv()

DEVS = [1668766845]
SUDO_USERS = []

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
MONGO_URL = os.getenv("MONGO_URL")
OWNER_ID = list(map(int, os.getenv("OWNER_ID").split()))
SUDO_USERS = list(map(int, os.getenv("SUDO_USERS", "").split()))
PREFIX = os.getenv("PREFIX", " . , : ; - ? *").split()
SESSION_STRING = os.getenv("SESSION_STRING")
BLACKLIST_CHAT = list(map(int, os.getenv("BLACKLIST_CHAT", "-1002124518138").split()))
MEMBERS = list(map(int, os.getenv("MEMBERS", "").split()))
LOG_GRP = int(os.getenv("LOG_GRP"))
