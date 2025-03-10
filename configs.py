from dotenv import load_dotenv
from os import path, getenv, mkdir


if path.exists("local.env"):
    load_dotenv("local.env")
else:
    load_dotenv()

if not path.exists("search"):
    mkdir("search")


class Configs:
    API_ID = int(getenv("API_ID", "0"))
    API_HASH = getenv("API_HASH", "abc123")
    BOT_TOKEN = getenv("BOT_TOKEN", "123:abc")
    DURATION_LIMIT = int(getenv('DURATION_LIMIT', '60'))
    OWNER_ID = int(getenv("OWNER_ID", "0123"))
    SESSION = getenv("SESSION", "session")
    CHANNEL_LINK = getenv("CHANNEL_LINK", "https://t.me/musickekiniaan")
    GROUP_LINK = getenv("GROUP_LINK", "https://t.me/Kekiniangroup")
    AUTO_LEAVE = int(getenv("AUTO_LEAVE", "1800"))


config = Configs()
