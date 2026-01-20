import random
import string
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, Message
from pytgcalls.exceptions import NoActiveGroupCall

import config
from Spy import Telegram, YouTube, app
from Spy.core.call import Sagar
from Spy.utils import seconds_to_min, time_to_seconds
from Spy.utils.decorators.play import PlayWrapper
from Spy.utils.formatters import formats
from Spy.utils.inline import (
    botplaylist_markup,
    livestream_markup,
    playlist_markup,
    slider_markup,
    track_markup,
)
from Spy.utils.logger import play_logs
from Spy.utils.stream.stream import stream

# Türk bayrağı emojisi
EMOJII = ["🇹🇷"]

yt_api = YouTube()  # YouTube.py’den sınıfı çağırıyoruz

@app.on_message(
    filters.command(["play", "vplay"]) & filters.group
)
@PlayWrapper
async def play_commnd(client, message: Message, _, chat_id, video, channel, playmode, url, fplay):
    Emoji = random.choice(EMOJII)
    mystic = await message.reply_text(_["play_2"].format(channel) if channel else Emoji)

    # Eğer reply ile Telegram dosyası atılmışsa
    if message.reply_to_message:
        audio_telegram = message.reply_to_message.audio or message.reply_to_message.voice
        video_telegram = message.reply_to_message.video or message.reply_to_message.document

        if audio_telegram:
            file_path = await Telegram.get_filepath(audio=audio_telegram)
            if await Telegram.download(_, message, mystic, file_path):
                details = {
                    "title": await Telegram.get_filename(audio_telegram, audio=True),
                    "link": await Telegram.get_link(message),
                    "path": file_path,
                    "dur": await Telegram.get_duration(audio_telegram, file_path),
                }
                await stream(_, mystic, message.from_user.id, details, chat_id,
                             message.from_user.first_name, message.chat.id,
                             streamtype="telegram", forceplay=fplay)
                return await mystic.delete()

        elif video_telegram:
            file_path = await Telegram.get_filepath(video=video_telegram)
            if await Telegram.download(_, message, mystic, file_path):
                details = {
                    "title": await Telegram.get_filename(video_telegram),
                    "link": await Telegram.get_link(message),
                    "path": file_path,
                    "dur": await Telegram.get_duration(video_telegram, file_path),
                }
                await stream(_, mystic, message.from_user.id, details, chat_id,
                             message.from_user.first_name, message.chat.id,
                             video=True, streamtype="telegram", forceplay=fplay)
                return await mystic.delete()

    # Eğer URL verilmişse
    if url:
        if await yt_api.exists(url):
            if "playlist" in url:
                # Playlist çalma
                try:
                    details = await yt_api.playlist(url, config.PLAYLIST_FETCH_LIMIT, message.from_user.id)
                except:
                    return await mystic.edit_text(_["play_3"])
                plist_type = "yt"
                plist_id = url.split("=")[1] if "=" in url else url
                await mystic.edit_text("» Playlist başlatılıyor...")
                # Playlist stream burada eklenebilir
            else:
                # Tek şarkı
                try:
                    _, stream_link = await yt_api.video(url)
                except:
                    return await mystic.edit_text(_["play_3"])
                details = {
                    "title": "Şarkı",
                    "link": url,
                    "path": stream_link
                }
                try:
                    # Sagar join ve stream
                    await Sagar.join_call(chat_id, stream_link, video=video)
                    await stream(_, mystic, message.from_user.id, details, chat_id,
                                 message.from_user.first_name, message.chat.id,
                                 video=video, streamtype="youtube", forceplay=fplay)
                except NoActiveGroupCall:
                    return await mystic.edit_text("❌ Sesli sohbet başlatılmamış.")
                except Exception as e:
                    return await mystic.edit_text(f"❌ Hata: {e}")
                await mystic.edit_text("🇹🇷 » Şarkı çalmaya başladı!")
                return

    # Eğer sadece arama yapılacaksa
    if not url and len(message.command) > 1:
        query = message.text.split(None, 1)[1]
        try:
            _, stream_link = await yt_api.video(query)
        except:
            return await mystic.edit_text(_["play_3"])
        details = {"title": query, "link": query, "path": stream_link}
        try:
            await Sagar.join_call(chat_id, stream_link, video=video)
            await stream(_, mystic, message.from_user.id, details, chat_id,
                         message.from_user.first_name, message.chat.id,
                         video=video, streamtype="youtube", forceplay=fplay)
        except Exception as e:
            return await mystic.edit_text(f"❌ Hata: {e}")
        await mystic.edit_text("🇹🇷 » Şarkı çalmaya başladı!")
        return

    # Eğer hiçbir şey yoksa inline playlist göster
    buttons = botplaylist_markup(_)
    await mystic.edit_text(_["play_18"], reply_markup=InlineKeyboardMarkup(buttons))
