import random
import string
import asyncio
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, InputMediaPhoto
from pytgcalls.exceptions import NoActiveGroupCall
from config import START_IMG_URL
import config
from YousefMusic import Apple, Resso, SoundCloud, Spotify, Telegram, YouTube, app
from YousefMusic.utils import seconds_to_min, time_to_seconds
from YousefMusic.utils.channelplay import get_channeplayCB
from YousefMusic.utils.decorators.language import languageCB, LanguageStart
from YousefMusic.utils.decorators.play import PlayWrapper
from YousefMusic.utils.formatters import formats
from YousefMusic.utils.inline.play import (
    livestream_markup,
    playlist_markup,
    slider_markup,
    track_markup,
)
from YousefMusic.utils.logger import play_logs
from YousefMusic.utils.stream.stream import stream
from config import BANNED_USERS, lyrical, CHANNEL_SUDO, YAFA_NAME, YAFA_CHANNEL
from YousefMusic.misc import SUDOERS
from YousefMusic.plugins.sudo.sudoers import sudoers_list
from YousefMusic.utils.inline import help_pannel, private_panel, start_pannel
from YousefMusic.utils.command import commandpro
from youtubesearchpython.future import VideosSearch

# تأكد من أن كل عنصر في الاستيراد موجود في نفس السطر أو مع فصل صحيح
from YousefMusic.utils.database import (
    add_served_chat,
    add_served_user,
    blacklisted_chats,
    get_assistant,
    get_lang,
    get_userss,
    is_on_off,
    is_served_private_chat,
    get_served_chats,
)
MESSAGE = f"""- اقوي بوت ميوزك قنوات و جروبات سرعه وجوده خارقه

وبدون تهنيج او تقطيع او توقف وكمان ان البوت في مميزات جامدة⚡️♥️.

ارفع البوت ادمن فقناتك او جروبك واستمتع بجوده الصوت و السرعه الخياليه للبوت ⚡️♥️

معرف البوت 🎸 [ @{app.username} ]

➤ 𝘉𝘰𝘵 𝘵𝘰 𝘱𝘭𝘢𝘺 𝘴𝘰𝘯𝘨𝘴 𝘪𝘯 𝘷𝘰𝘪𝘤e 𝘤𝘩𝘢𝘵 ♩🎸 \n\n-𝙱𝙾𝚃 ➤ @{app.username}"""

BUTTON = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("اضف البوت الي مجموعتك او قناتك ❤️✨", url=f"https://t.me/{app.username}?startgroup=True")
        ]
    ]
)

async def send_message_to_chats():
    try:
        chats = await get_served_chats()  # Retrieve the served chats
        for chat_info in chats:
            chat_id = chat_info.get('chat_id')
            if isinstance(chat_id, int):
                try:
                    await app.send_photo(chat_id, photo=START_IMG_URL, caption=MESSAGE, reply_markup=BUTTON)
                    await asyncio.sleep(3)
                except Exception:
                    pass
    except Exception:
        pass

@app.on_message(filters.command(["اعلان للبوت"], ""))
async def auto_broadcast_command(client: Client, message: Message):
    await message.reply("تم بدء نشر اعلان للبوت في جميع المجموعات والقنوات، يرجى عدم تكرار الامر")
    await send_message_to_chats()
    await message.reply("تم الانتهاء من الاعلان في جميع خاص المستخزمين والمجموعات والقنوات")
