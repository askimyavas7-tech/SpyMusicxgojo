import re
from os import getenv

from dotenv import load_dotenv
from pyrogram import filters

load_dotenv()


API_ID = int(getenv("API_ID", "35279715"))

API_HASH = getenv("API_HASH", "b4c339216397b5941d88c8617d2dc12b")

BOT_TOKEN = getenv("BOT_TOKEN", "")

MONGO_DB_URI = getenv("MONGO_DB_URI", "mongodb+srv://knight4563:knight4563@cluster0.a5br0se.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

DURATION_LIMIT_MIN = int(getenv("DURATION_LIMIT", 54000))

SONG_DOWNLOAD_DURATION = int(
    getenv("SONG_DOWNLOAD_DURATION_LIMIT", "54000")
)

LOGGER_ID = int(getenv("LOGGER_ID", "-1003228624224"))

OWNER_ID = int(getenv("OWNER_ID", "7651303468"))

BOT_USERNAME = getenv("BOT_USERNAME" , "gojo_x_jinwoo_bot")

COMMAND_HANDLER = getenv("COMMAND_HANDLER", "! / .").split()

HEROKU_APP_NAME = getenv("HEROKU_APP_NAME")

HEROKU_API_KEY = getenv("HEROKU_API_KEY")

UPSTREAM_REPO = getenv(
    "UPSTREAM_REPO",
    "",
)
UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "https://github.com/itzarjuna1/SpyMusicxgojo")
GIT_TOKEN = getenv(
    "GIT_TOKEN", ""
)  # Fill this variable if your upstream repository is private

SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/dark_musictm")
SUPPORT_CHAT = getenv("SUPPORT_CHAT", "https://t.me/snowy_hometown")

AUTO_LEAVING_ASSISTANT = bool(getenv("AUTO_LEAVING_ASSISTANT", False))
AUTO_SUGGESTION_MODE = getenv("AUTO_SUGGESTION_MODE", "True")
AUTO_SUGGESTION_TIME = int(
    getenv("AUTO_SUGGESTION_TIME", "500"))

SPOTIFY_CLIENT_ID = getenv("SPOTIFY_CLIENT_ID", "6fb7e1766693439b86ec57e3deb3c36f")
SPOTIFY_CLIENT_SECRET = getenv("SPOTIFY_CLIENT_SECRET", "da3f94c6a68d49f6b64a7216ec9eb905")



PLAYLIST_FETCH_LIMIT = int(getenv("PLAYLIST_FETCH_LIMIT", 25))

CLEANMODE_DELETE_MINS = int(
    getenv("CLEANMODE_MINS", "5"))

TG_AUDIO_FILESIZE_LIMIT = int(getenv("TG_AUDIO_FILESIZE_LIMIT", 21474836480))
TG_VIDEO_FILESIZE_LIMIT = int(getenv("TG_VIDEO_FILESIZE_LIMIT", 21474836480))



# Get your pyrogram v2 session from @Shsusu_bot on Telegram
STRING1 = getenv("STRING_SESSION", "")
STRING2 = getenv("STRING_SESSION2", None)
STRING3 = getenv("STRING_SESSION3", None)
STRING4 = getenv("STRING_SESSION4", None)
STRING5 = getenv("STRING_SESSION5", None)


BANNED_USERS = filters.user()
adminlist = {}
lyrical = {}
votemode = {}
autoclean = []
confirmer = {}
chatstats = {}
userstats = {}
clean = {}

autoclean = []

START_IMG_URL = getenv(
    "START_IMG_URL", "https://files.catbox.moe/k8ix72.jpg"
)
PING_IMG_URL = getenv(
    "PING_IMG_URL", "https://files.catbox.moe/k8ix72.jpg"
)
PLAYLIST_IMG_URL = "https://files.catbox.moe/k8ix72.jpg"
STATS_IMG_URL = "https://files.catbox.moe/k8ix72.jpg"
TELEGRAM_AUDIO_URL = "https://files.catbox.moe/k8ix72.jpg"
TELEGRAM_VIDEO_URL = "https://files.catbox.moe/k8ix72.jpg"
STREAM_IMG_URL = "https://files.catbox.moe/k8ix72.jpg"
SOUNCLOUD_IMG_URL = "https://files.catbox.moe/k8ix72.jpg"
YOUTUBE_IMG_URL = "https://files.catbox.moe/k8ix72.jpg"
SPOTIFY_ARTIST_IMG_URL = "https://files.catbox.moe/k8ix72.jpg"
SPOTIFY_ALBUM_IMG_URL = "https://files.catbox.moe/k8ix72.jpg"
SPOTIFY_PLAYLIST_IMG_URL = "https://files.catbox.moe/k8ix72.jpg"


def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60**i for i, x in enumerate(reversed(stringt.split(":"))))


DURATION_LIMIT = int(time_to_seconds(f"{DURATION_LIMIT_MIN}:00"))
SONG_DOWNLOAD_DURATION_LIMIT = int(
    time_to_seconds(f"{SONG_DOWNLOAD_DURATION}:00"))

if SUPPORT_CHANNEL:
    if not re.match("(?:http|https)://", SUPPORT_CHANNEL):
        raise SystemExit(
            "[ERROR] - Your SUPPORT_CHANNEL url is wrong. Please ensure that it starts with https://"
        )

if SUPPORT_CHAT:
    if not re.match("(?:http|https)://", SUPPORT_CHAT):
        raise SystemExit(
            "[ERROR] - Your SUPPORT_CHAT url is wrong. Please ensure that it starts with https://"
        )
