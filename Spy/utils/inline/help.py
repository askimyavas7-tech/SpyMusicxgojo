from Spy import app
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


# ================= FIRST PAGE ================= #

def first_page(_):
    controll_button = [
        InlineKeyboardButton("◁", callback_data="Adisa"),
        InlineKeyboardButton("HOME", callback_data="settingsback_helper"),
        InlineKeyboardButton("▷", callback_data="dilXaditi"),
    ]

    first_page_menu = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(_.get("H_B_1", "🎵 Music"), callback_data="help_callback hb1"),
                InlineKeyboardButton(_.get("H_B_2", "🛠 Admin"), callback_data="help_callback hb2"),
                InlineKeyboardButton(_.get("H_B_3", "⚙ Settings"), callback_data="help_callback hb3"),
            ],
            [
                InlineKeyboardButton(_.get("H_B_4", "📊 Stats"), callback_data="help_callback hb4"),
                InlineKeyboardButton(_.get("H_B_5", "👥 Group"), callback_data="help_callback hb5"),
                InlineKeyboardButton(_.get("H_B_6", "👤 User"), callback_data="help_callback hb6"),
            ],
            [
                InlineKeyboardButton(_.get("H_B_7", "🤖 Bot"), callback_data="help_callback hb7"),
                InlineKeyboardButton(_.get("H_B_8", "🔙 Back"), callback_data="help_callback home"),
            ],
            controll_button,
        ]
    )
    return first_page_menu


# ================= SECOND PAGE ================= #

def second_page(_):
    controll_button = [
        InlineKeyboardButton("◁", callback_data="settings_back_helper_fixed"),
        InlineKeyboardButton("HOME", callback_data="settingsback_helper"),
        InlineKeyboardButton("▷", callback_data="settings_back_helper"),
    ]

    second_page_menu = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(_.get("H_B_10", "🎧 Audio"), callback_data="help_callback hb10"),
                InlineKeyboardButton(_.get("H_B_11", "📂 Playlist"), callback_data="help_callback hb11"),
                InlineKeyboardButton(_.get("H_B_12", "🔊 Voice"), callback_data="help_callback hb12"),
            ],
            [
                InlineKeyboardButton(_.get("H_B_13", "🧠 AI"), callback_data="help_callback hb13"),
                InlineKeyboardButton(_.get("H_B_14", "⚡ Speed"), callback_data="help_callback hb14"),
                InlineKeyboardButton(_.get("H_B_15", "🛡 Security"), callback_data="help_callback hb15"),
            ],
            [
                InlineKeyboardButton(_.get("H_B_16", "ℹ Info"), callback_data="help_callback hb16"),
            ],
            controll_button,
        ]
    )
    return second_page_menu


# ================= BACK BUTTON ================= #

def help_back_markup(_):
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton(_.get("BACK_BUTTON", "🔙 Back"), callback_data="settings_back_helper")]]
    )


# ================= PRIVATE PANEL ================= #

def private_help_panel(_):
    return [
        [
            InlineKeyboardButton(
                _.get("S_B_4", "⚙ Settings"),
                url=f"https://t.me/{app.username}?start=help",
            )
        ]
	]
