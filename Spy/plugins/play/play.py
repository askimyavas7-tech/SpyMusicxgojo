# play.py - SpyMusicxGojo için düzeltilmiş versiyon 🇹🇷

import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from Spy.utils.decorators import admin_only  # ✅ Düzeltilmiş dekoratör importu
from Spy.platforms.youtube import YouTubeAPI  # ✅ YouTubeAPI doğru import
from Spy.platforms.spotify import SpotifyAPI
from Spy.platforms.soundcloud import SoundAPI
from Spy.platforms.apple import AppleAPI
from Spy.platforms.carbon import CarbonAPI
from Spy.platforms.resso import RessoAPI
from Spy.platforms.telegram import TeleAPI

# Bot instance (pyrogram Client)
app = Client("SpyMusicBot")

# Yardımcı fonksiyon: şarkı oynatma
async def play_song(chat_id: int, query: str):
    """
    Kullanıcı bir şarkı isteğinde bulunduğunda çalışır.
    Sırasıyla platformlarda arar ve link döndürür.
    """
    # YouTube'da arama
    yt_result = await YouTubeAPI.search(query)
    if yt_result:
        return await YouTubeAPI.stream(yt_result[0]["url"])

    # Spotify araması
    sp_result = await SpotifyAPI.search(query)
    if sp_result:
        return await SpotifyAPI.stream(sp_result[0]["url"])

    # SoundCloud araması
    sc_result = await SoundAPI.search(query)
    if sc_result:
        return await SoundAPI.stream(sc_result[0]["url"])

    # Apple Music araması
    am_result = await AppleAPI.search(query)
    if am_result:
        return await AppleAPI.stream(am_result[0]["url"])

    # Carbon Music araması
    cb_result = await CarbonAPI.search(query)
    if cb_result:
        return await CarbonAPI.stream(cb_result[0]["url"])

    # Resso Music araması
    rs_result = await RessoAPI.search(query)
    if rs_result:
        return await RessoAPI.stream(rs_result[0]["url"])

    # Telegram Music araması
    tg_result = await TeleAPI.search(query)
    if tg_result:
        return await TeleAPI.stream(tg_result[0]["url"])

    return None

# Komut: /play
@app.on_message(filters.command("play") & filters.private)
@admin_only  # Sadece adminler kullanabilir
async def play_handler(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply("Şarkı adı yazmalısın! 🇹🇷")
        return

    query = " ".join(message.command[1:])
    await message.reply(f"Aranıyor: {query} 🇹🇷")

    try:
        stream_url = await play_song(message.chat.id, query)
        if stream_url:
            await message.reply(f"Şarkı hazır! Dinle: {stream_url} 🇹🇷")
        else:
            await message.reply("Şarkı bulunamadı. 🇹🇷")
    except Exception as e:
        await message.reply(f"Hata oluştu: {str(e)} 🇹🇷")

# Botu çalıştır
if __name__ == "__main__":
    print("SpyMusicBot 🇹🇷 başlatılıyor...")
    app.run()
