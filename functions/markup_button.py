from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from configs import config
from database.lang_utils import get_message as gm


def music_or_video_keyboard(user_id: int, streaming_status: str):
    keyboard = []
    number = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]
    for count, j in enumerate(number):
        keyboard.append(
            InlineKeyboardButton(
                f"{j}", callback_data=f"{streaming_status} {count}|{user_id}"
            )
        )
    return keyboard


def process_button(user_id: int, streaming_status: str):
    board = music_or_video_keyboard(user_id, streaming_status)
    temp = []
    keyboard = []
    for count, button in enumerate(board, start=1):
        temp.append(button)
        if count % 3 == 0:
            keyboard.append(temp)
            temp = []
        if count == len(board):
            keyboard.append(temp)
    return keyboard


def start_markup(chat_id: int, bot_username: str):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    gm(chat_id, "➕ ᴀᴅᴅ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ➕"),
                    url=f"https://t.me/{bot_username}?startgroup=true",
                )
            ],
            [
                InlineKeyboardButton(gm(chat_id, "helpbutton"), callback_data="cbhelp"),
                InlineKeyboardButton(
                    gm(chat_id, "👑ᴏᴡɴᴇʀ👑"), url="https://t.me/rumahakhirat"
                ),
            ],
            [
                InlineKeyboardButton(gm(chat_id, "🔰ᴄʜᴀɴɴᴇʟ🔰"), url=config.CHANNEL_LINK),
                InlineKeyboardButton(
                    gm(chat_id, "🔰ꜱᴜᴘᴘᴏʀᴛ🔰"), url=config.GROUP_LINK
                )
            ],
        ]
    )
