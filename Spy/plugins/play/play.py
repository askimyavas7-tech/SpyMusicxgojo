import random
import string
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, Message
from pytgcalls.exceptions import NoActiveGroupCall

import config
from Spy import Apple, Resso, SoundCloud, Spotify, Telegram, YouTube
from Spy.utils.decorators.play import PlayWrapper
from Spy.utils.decorators.language import languageCB
from Spy.core.call import Sagar
from Spy.utils.stream.stream import stream
from Spy.utils.channelplay import get_channeplayCB
from Spy.utils.formatters import formats, time_to_seconds
from Spy.utils.logger import play_logs
from Spy.utils import seconds_to_min

# Türk bayrağı emojisi
EMOJII = ["🇹🇷"]

# YouTubeAPI örneği
yt_api = YouTube.YouTubeAPI()  # DÜZELTİLDİ: artık YouTubeAPI sınıfı doğru şekilde çağrılıyor

@app.on_message(
    filters.command(
        [
            "play",
            "vplay",
            "cplay",
            "cvplay",
            "playforce",
            "vplayforce",
            "cplayforce",
            "cvplayforce",
        ]
    )
    & filters.group
    & ~config.BANNED_USERS
)
@PlayWrapper
async def play_command(
    client,
    message: Message,
    _,
    chat_id,
    video,
    channel,
    playmode,
    url,
    fplay,
):
    Emoji = random.choice(EMOJII)
    mystic = await message.reply_text(_["play_2"].format(channel) if channel else Emoji)

    # Reply ile gönderilen Telegram dosyaları
    audio_telegram = (message.reply_to_message.audio or message.reply_to_message.voice) if message.reply_to_message else None
    video_telegram = (message.reply_to_message.video or message.reply_to_message.document) if message.reply_to_message else None

    user_id = message.from_user.id
    user_name = message.from_user.mention

    if audio_telegram:
        if audio_telegram.file_size > 104857600:
            return await mystic.edit_text(_["play_5"])
        duration_min = seconds_to_min(audio_telegram.duration)
        if audio_telegram.duration > config.DURATION_LIMIT:
            return await mystic.edit_text(_["play_6"].format(config.DURATION_LIMIT_MIN, app.mention))
        file_path = await Telegram.get_filepath(audio=audio_telegram)
        if await Telegram.download(_, message, mystic, file_path):
            details = {
                "title": await Telegram.get_filename(audio_telegram, audio=True),
                "link": await Telegram.get_link(message),
                "path": file_path,
                "dur": await Telegram.get_duration(audio_telegram, file_path),
            }
            try:
                await stream(_, mystic, user_id, details, chat_id, user_name, message.chat.id, streamtype="telegram", forceplay=fplay)
            except Exception as e:
                ex_type = type(e).__name__
                err = e if ex_type == "AssistantErr" else _["general_2"].format(ex_type)
                return await mystic.edit_text(err)
            return await mystic.delete()

    elif video_telegram:
        if video_telegram.file_size > config.TG_VIDEO_FILESIZE_LIMIT:
            return await mystic.edit_text(_["play_8"])
        file_path = await Telegram.get_filepath(video=video_telegram)
        if await Telegram.download(_, message, mystic, file_path):
            details = {
                "title": await Telegram.get_filename(video_telegram),
                "link": await Telegram.get_link(message),
                "path": file_path,
                "dur": await Telegram.get_duration(video_telegram, file_path),
            }
            try:
                await stream(_, mystic, user_id, details, chat_id, user_name, message.chat.id, video=True, streamtype="telegram", forceplay=fplay)
            except Exception as e:
                ex_type = type(e).__name__
                err = e if ex_type == "AssistantErr" else _["general_2"].format(ex_type)
                return await mystic.edit_text(err)
            return await mystic.delete()

    elif url:
        if await yt_api.exists(url):
            if "playlist" in url:
                try:
                    details = await yt_api.playlist(url, config.PLAYLIST_FETCH_LIMIT, message.from_user.id)
                    streamtype = "playlist"
                    cap = _["play_9"]
                    img = config.PLAYLIST_IMG_URL
                except:
                    return await mystic.edit_text(_["play_3"])
            else:
                try:
                    details, track_id = await yt_api.track(url)
                    streamtype = "youtube"
                    cap = _["play_10"].format(details["title"], details["duration_min"])
                    img = details["thumb"]
                except:
                    return await mystic.edit_text(_["play_3"])
        else:
            return await mystic.edit_text(_["play_3"])
        try:
            await stream(_, mystic, user_id, details, chat_id, user_name, message.chat.id, video=video, streamtype=streamtype, forceplay=fplay)
        except Exception as e:
            ex_type = type(e).__name__
            err = e if ex_type == "AssistantErr" else _["general_2"].format(ex_type)
            return await mystic.edit_text(err)
        return await mystic.delete()
