# play.py

import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message

from Spy.platforms.YouTube import YouTubeAPI  # ✅ Düzeltildi
from Spy.utils.database import is_on_off
from Spy.utils.formatters import time_to_seconds

yt_api = YouTubeAPI()  # artık doğru şekilde çağrılıyor

# Komut: /play
@Client.on_message(filters.command("play") & filters.group)
async def play(client: Client, message: Message):
    user = message.from_user
    chat_id = message.chat.id

    # Mesaj yanıtı veya link kontrolü
    if not message.reply_to_message and len(message.command) < 2:
        await message.reply_text("» Lütfen bir kullanıcıya yanıt verin veya geçerli bir şarkı linki gönderin 🇹🇷")
        return

    # Link veya başlık al
    song_input = message.text.split(None, 1)[1] if len(message.command) > 1 else None
    if message.reply_to_message:
        song_input = message.reply_to_message.text or song_input

    # Arama mesajı
    status_msg = await message.reply_text("» Şarkınız aranıyor... 🇹🇷")

    try:
        # YouTube detaylarını al
        title, duration_min, duration_sec, thumbnail, vidid = await yt_api.details(song_input)

        # Sıra mesajı
        await status_msg.edit_text(f"» Şimdi çalınıyor: {title} 🇹🇷")

        # Şarkıyı indir
        audio_file, success = await yt_api.download(song_input, mystic=True)

        if success:
            await client.send_audio(
                chat_id,
                audio_file,
                title=title,
                duration=duration_sec,
                caption=f"🎵 {title} çalınıyor 🇹🇷"
            )
            await status_msg.delete()
        else:
            await status_msg.edit_text(f"❌ Şarkı indirilemedi: {audio_file} 🇹🇷")

    except Exception as e:
        await status_msg.edit_text(f"❌ Bir hata oluştu: {e} 🇹🇷")
