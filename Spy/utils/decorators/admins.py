# admin.py
from functools import wraps
from pyrogram.types import Message, CallbackQuery
from Spy import app
from Spy.misc import SUDOERS, confirmer, db
from Spy.utils.database import get_lang, is_maintenance, is_active_chat, is_nonadmin_chat, is_skipmode, get_upvote_count, get_cmode
from config import SUPPORT_CHAT, adminlist
from strings import get_string
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from ..formatters import int_to_alpha


def admin_only(func):
    @wraps(func)
    async def wrapper(client, message: Message, *args, **kwargs):
        if await is_maintenance() is False and message.from_user.id not in SUDOERS:
            return await message.reply_text(
                text=f"{app.mention} is under maintenance, visit <a href={SUPPORT_CHAT}>support chat</a> to know the reason.",
                disable_web_page_preview=True,
            )

        # Try deleting message
        try:
            await message.delete()
        except:
            pass

        # Language
        try:
            lang = await get_lang(message.chat.id)
            _ = get_string(lang)
        except:
            _ = get_string("en")

        # Admin checks
        if message.sender_chat:
            upl = InlineKeyboardMarkup([[InlineKeyboardButton(text="How to fix?", callback_data="SagarmousAdmin")]])
            return await message.reply_text(_["general_3"], reply_markup=upl)

        # Chat ID for /c commands
        if message.command[0][0] == "c":
            chat_id = await get_cmode(message.chat.id)
            if chat_id is None:
                return await message.reply_text(_["setting_7"])
            try:
                await app.get_chat(chat_id)
            except:
                return await message.reply_text(_["cplay_4"])
        else:
            chat_id = message.chat.id

        if not await is_active_chat(chat_id):
            return await message.reply_text(_["general_5"])

        is_non_admin = await is_nonadmin_chat(message.chat.id)
        if not is_non_admin and message.from_user.id not in SUDOERS:
            admins = adminlist.get(message.chat.id)
            if not admins:
                return await message.reply_text(_["admin_13"])
            elif message.from_user.id not in admins:
                if await is_skipmode(message.chat.id):
                    upvote = await get_upvote_count(chat_id)
                    text = f"<b>Admin rights needed</b>\n\n» {upvote} votes needed for this action."
                    command = message.command[0]
                    if command[0] == "c":
                        command = command[1:]
                    MODE = command.title()
                    upl = InlineKeyboardMarkup([[InlineKeyboardButton(text="Vote", callback_data=f"ADMIN UpVote|{chat_id}_{MODE}")]])
                    if chat_id not in confirmer:
                        confirmer[chat_id] = {}
                    try:
                        vidid = db[chat_id][0]["vidid"]
                        file = db[chat_id][0]["file"]
                    except:
                        return await message.reply_text(_["admin_14"])
                    senn = await message.reply_text(text, reply_markup=upl)
                    confirmer[chat_id][senn.id] = {"vidid": vidid, "file": file}
                    return
                else:
                    return await message.reply_text(_["admin_14"])

        return await func(client, message, *args, **kwargs)

    return wrapper
