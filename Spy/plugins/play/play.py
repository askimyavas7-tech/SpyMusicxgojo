from pyrogram import Client, filters
from Spy.platforms.YouTube import YouTubeAPI
from Spy.core.call import Call

yt_api = YouTubeAPI()

# Basit admin kontrol fonksiyonu
async def admin_only_check(client, message):
    member = await client.get_chat_member(message.chat.id, message.from_user.id)
    if not member.status in ("administrator", "creator"):
        await message.reply_text("Bu komutu kullanmak için admin olmalısın 🇹🇷")
        return False
    return True

@Client.on_message(filters.command("play") & filters.group)
async def play(client, message):
    if not await admin_only_check(client, message):
        return

    query = " ".join(message.command[1:])
    if not query:
        await message.reply_text("Lütfen çalmak istediğin şarkının adını yaz 🇹🇷")
        return

    try:
        video = await yt_api.search(query)
    except Exception as e:
        await message.reply_text(f"Arama sırasında bir hata oluştu: {e} 🇹🇷")
        return

    if not video:
        await message.reply_text("Şarkı bulunamadı 🇹🇷")
        return

    try:
        await Call.stream(message.chat.id, video.url)
        await message.reply_text(f"🎵 Şimdi çalıyor 🇹🇷 **{video.title}**")
    except Exception as e:
        await message.reply_text(f"Şarkı çalınamadı: {e} 🇹🇷")
