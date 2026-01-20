# Spy/plugins/play/play.py

import asyncio
from pyrogram import Client, filters
from Spy.platforms.Youtube import YouTubeAPI  # ✅ Düzeltildi, dosya ismi doğru
from Spy.core.call import Call
from Spy.utils.decorators import admin_only

# YouTube API sınıfını başlatıyoruz
yt_api = YouTubeAPI()

# Türk bayrağı eklendi
NOW_PLAYING = "🎵 Şimdi çalıyor 🇹🇷:"

@Client.on_message(filters.command("play") & filters.group)
@admin_only
async def play(client, message):
    # Kullanıcının mesajını alıyoruz
    query = " ".join(message.command[1:])
    if not query:
        await message.reply_text("Lütfen çalmak istediğin şarkının adını yaz 🇹🇷")
        return

    # Youtube üzerinden arama
    try:
        video = await yt_api.search(query)
    except Exception as e:
        await message.reply_text(f"Hata oluştu: {e} 🇹🇷")
        return

    if not video:
        await message.reply_text("Şarkı bulunamadı 🇹🇷")
        return

    # Şarkıyı oynatma
    try:
        await Call.stream(message.chat.id, video.url)
        await message.reply_text(f"{NOW_PLAYING} **{video.title}**")
    except Exception as e:
        await message.reply_text(f"Şarkı çalınamadı: {e} 🇹🇷")
