from pyrogram.types import InlineKeyboardButton

import config
from Spy import app


def start_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text=_.get("S_B_1", "➕ Gruba Ekle"),
                url=f"https://t.me/{app.username}?startgroup=true",
            ),
            InlineKeyboardButton(
                text=_.get("S_B_2", "💬 Destek"),
                url=config.SUPPORT_CHAT,
            ),
        ],
    ]
    return buttons


def private_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text=_.get("S_B_3", "➕ Beni Gruba Ekle"),
                url=f"https://t.me/{app.username}?startgroup=true",
            )
        ],
        [
            InlineKeyboardButton(
                text=_.get("S_B_4", "⚙️ Ayarlar"),
                callback_data="settings_back_helper",
            )
        ],
        [
            InlineKeyboardButton(
                text=_.get("S_B_2", "🌐 Dil"),
                callback_data="dil_spy",
            ),
            InlineKeyboardButton(
                text=_.get("S_B_7", "📦 Kaynak"),
                callback_data="gib_source",
            ),
        ],
        [
            InlineKeyboardButton("• ʙᴏᴛ ɪɴғᴏ •", callback_data="bot_info_data"),
        ],
    ]
    return buttons
