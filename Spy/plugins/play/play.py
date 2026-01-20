# Spy/plugins/play/play.py
import asyncio
import os
from pyrogram import Client, filters
from pyrogram.types import Message
from Spy.platforms.youtube import YouTubeAPI  # ✅ Küçük harfe çevrildi
from Spy.utils.decorators.admin import admin_only  # ✅ Doğru dekoratör yolu
from Spy.utils.database import is_on_off
from Spy.utils.formatters import time_to_seconds

YT = YouTubeAPI()

@Client.on_message(filters.command("play") & filters.group)
@admin_only  # Sadece adminler kullanabilir
async def play(_, message: Message):
    # 🎵 Müziği arıyor
    await message.reply_text("🎶 Şarkı aranıyor... 🇹🇷")

    text = message.text.split(None, 1)
    if len(text) < 2:
        return await message.reply_text("❌ Lütfen bir şarkı ismi veya link girin!")

    query = text[1]

    # Link veya arama
    if "youtube.com" in query or "youtu.be" in query:
        url = query
    else:
        search_result = await YT.details(query)
        url = f"https://www.youtube.com/watch?v={search_result[4]}"  # video id

    # Müziği indir
    try:
        file_path, success = await YT.download(url, mystic=None)
    except Exception as e:
        return await message.reply_text(f"❌ Şarkı indirilemedi: {e}")

    if success:
        await message.reply_audio(
            audio=file_path,
            caption=f"🎵 Şarkı çalınıyor... 🇹🇷\n**{query}**"
        )
    else:
        await message.reply_text("❌ Şarkı indirilemedi!")
