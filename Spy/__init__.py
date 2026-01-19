from Spy.core.bot import Sagar
from Spy.core.dir import dirr
from Spy.core.userbot import Userbot
from Spy.misc import dbb, heroku

from .logging import LOGGER

# ================= SAFE STARTUP CORE =================

try:
    dirr()
except Exception as e:
    LOGGER(__name__).warning(f"Directory init skipped: {e}")

try:
    from Spy.core.git import git
    git()
except Exception as e:
    LOGGER(__name__).warning(f"Git system skipped: {e}")

try:
    dbb()
except Exception as e:
    LOGGER(__name__).error(f"Database init failed: {e}")
    raise e

try:
    heroku()
except Exception as e:
    LOGGER(__name__).warning(f"Heroku helper skipped: {e}")

app = Sagar()
userbot = Userbot()

# ================= PLATFORM SYSTEM (CRITICAL FIX) =================

# Önce hepsini None olarak tanımla (ImportError'u engeller)
Apple = None
Carbon = None
SoundCloud = None
Spotify = None
Resso = None
Telegram = None
YouTube = None

try:
    from .platforms import (
        AppleAPI,
        CarbonAPI,
        SoundAPI,
        SpotifyAPI,
        RessoAPI,
        TeleAPI,
        YouTubeAPI,
    )

    Apple = AppleAPI()
    Carbon = CarbonAPI()
    SoundCloud = SoundAPI()
    Spotify = SpotifyAPI()
    Resso = RessoAPI()
    Telegram = TeleAPI()
    YouTube = YouTubeAPI()

    LOGGER(__name__).info("All platform APIs loaded successfully")

except Exception as e:
    LOGGER(__name__).error(f"Platform API load failed: {e}")

# ================= FAIL-SAFE DUMMY OBJECTS =================

class DummyPlatform:
    async def search(self, *args, **kwargs):
        raise RuntimeError("Platform API not loaded")

    async def download(self, *args, **kwargs):
        raise RuntimeError("Platform API not loaded")

# Eğer herhangi biri yüklenmediyse dummy ata
if YouTube is None:
    LOGGER(__name__).warning("YouTube API missing, using DummyPlatform")
    YouTube = DummyPlatform()

if Spotify is None:
    Spotify = DummyPlatform()

if SoundCloud is None:
    SoundCloud = DummyPlatform()

if Telegram is None:
    Telegram = DummyPlatform()
