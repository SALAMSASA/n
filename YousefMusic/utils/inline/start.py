
from YousefMusic import app
from typing import Union
from pyrogram.types import InlineKeyboardButton
from config import YAFA_CHANNEL, SUPPORT_CHAT, OWNER_ID


def start_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_1"],
                url=f"https://t.me/{app.username}?start=help",
            )
        ],
        [
            InlineKeyboardButton(text=_["S_B_2"], callback_data="settings_helper"),
            InlineKeyboardButton(text=_["S_B_4"], url=f"{YAFA_CHANNEL}"),
        ],
        [
            InlineKeyboardButton(text=_["S_B_3"], url=f"{SUPPORT_CHAT}"),
        ],
        [
            InlineKeyboardButton(
                text="‹ مطور البوت ›", url=f"https://t.me/H_8_o"
            ),
            InlineKeyboardButton(
                text="‹ مطور السورس ›", url=f"https://t.me/H_8_o"
            ),
        ],
    ]
    return buttons


def private_panel(_, OWNER_ID: Union[bool, int] = None):
    buttons = [
        [InlineKeyboardButton(text=_["S_B_8"], callback_data="zzzback")],
        [
            InlineKeyboardButton(text=_["S_B_4"], url=f"{YAFA_CHANNEL}"),
            InlineKeyboardButton(text=_["S_B_3"], url=f"{SUPPORT_CHAT}"),
        ],
        [
            InlineKeyboardButton(
                text=_["S_B_5"],
                url=f"https://t.me/{app.username}?startgroup=true",
            )
        ],
        [
            InlineKeyboardButton(
                text="‹ مطور البوت ›", url=f"https://t.me/H_8_o"
            ),
            InlineKeyboardButton(
                text="‹ مطور السورس ›", url=f"https://t.me/H_8_o"
            ),
        ],
        [
            InlineKeyboardButton(text=_["S_B_7"], user_id=OWNER_ID),
            InlineKeyboardButton(text=_["S_B_6"], url=f"https://t.me/H_8_o"),
        ] if OWNER_ID else [],
        [InlineKeyboardButton(text=_["ST_B_6"], callback_data="LG")],
    ]
    return buttons


def alive_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text="- اضفني .", url=f"https://t.me/{app.username}?startgroup=true"
            ),
            InlineKeyboardButton(text=_["S_B_3"], url=f"{SUPPORT_CHAT}"),
        ],
    ]
    return buttons
