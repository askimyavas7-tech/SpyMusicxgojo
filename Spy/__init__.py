from Spy.core.bot import Sagar
from Spy.core.dir import dirr
from Spy.core.userbot import Userbot
from Spy.misc import dbb, heroku

from .logging import LOGGER

# Güvenli başlangıç sırası

try:
    dirr()
except Exception as e:
    LOGGER(__name__).warning(f"Directory init skipped: {e}")

# Git sistemi Heroku'da uyumsuz olduğu için güvenli şekilde atlanır
try:
    from Spy.core.git import git
    git()
except Exception as e:
    LOGGER(__name__).warning(f"Git system skipped: {e}")

try:
    dbb()
except Exception as e:
    LOGGER(__name__).error(f"Database init failed: {e}")
    raise e  # DB olmadan bot çalışmaz

try:
    heroku()
except Exception as e:
    LOGGER(__name__).warning(f"Heroku helper skipped: {e}")

# Ana botlar
app = Sagar()
userbot = Userbot()

# Platform API'leri güvenli yükle
try:
    from .platforms import *

    Apple = AppleAPI()
    Carbon = CarbonAPI()
    SoundCloud = SoundAPI()
    Spotify = SpotifyAPI()
    Resso = RessoAPI()
    Telegram = TeleAPI()
    YouTube = YouTubeAPI()
except Exception as e:
    LOGGER(__name__).error(f"Platform APIs failed to load: {e}")
