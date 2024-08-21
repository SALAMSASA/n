import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from config import START_IMG_URL, BANNED_USERS, CHANNEL_SUDO, YAFA_NAME, YAFA_CHANNEL
from YousefMusic import app
from YousefMusic.core.call import Zelzaly
from YousefMusic.utils import seconds_to_min, time_to_seconds
from YousefMusic.utils.channelplay import get_channeplayCB
from YousefMusic.utils.database import get_served_chats
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
from strings import get_command, get_string
from YousefMusic.misc import SUDOERS
from YousefMusic.plugins.play.playlist import del_plist_msg
from YousefMusic.plugins.sudo.sudoers import sudoers_list
from YousefMusic.utils.database import (
    add_served_chat,
    add_served_user,
    blacklisted_chats,
    get_assistant,
    get_lang,
    get_userss,
    is_on_off,
    is_served_private_chat,
)
from YousefMusic.utils.inline import help_pannel, private_panel, start_pannel
from YousefMusic.utils.command import commandpro
from youtubesearchpython.__future__ import VideosSearch

# الرسالة التي سيتم إرسالها
MESSAGE = f"""- اقوي بوت ميوزك قنوات و جروبات سرعه وجوده خارقه

وبدون تهنيج او تقطيع او توقف وكمان ان البوت في مميزات جامدة⚡️♥️.

ارفع البوت ادمن فقناتك او جروبك واستمتع بجوده الصوت و السرعه الخياليه للبوت ⚡️♥️

معرف البوت 🎸 [ @{app.username} ]

➤ 𝘉𝘰𝘁 𝘁𝘰 𝘱𝘭𝘢𝘆 𝘀𝘂𝘁 𝘃𝘂𝘁𝘀 𝘁𝘰 𝘃𝘂𝘁𝘀 ♩🎸 \n\n-𝙱𝙾𝚃 ➤ @{app.username}"""

# زر لتوجيه المستخدمين إلى رابط البوت
BUTTON = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("اضف البوت الي مجموعتك او قناتك ❤️✨", url=f"https://t.me/{app.username}?startgroup=True")
        ]
    ]
)

# دالة لإرسال الرسائل إلى المحادثات
async def send_message_to_chats():
    try:
        chats = await get_served_chats()
        for chat_info in chats:
            chat_id = chat_info.get('chat_id')
            if isinstance(chat_id, int):
                try:
                    await app.send_photo(chat_id, photo=START_IMG_URL, caption=MESSAGE, reply_markup=BUTTON)
                    await asyncio.sleep(3)
                except Exception as e:
                    play_logs.error(f"Error sending message to chat {chat_id}: {e}")
    except Exception as e:
        play_logs.error(f"Error in send_message_to_chats: {e}")

# دالة للتعامل مع أمر نشر الإعلان
@app.on_message(filters.command(["اعلان للبوت"], ""))
async def auto_broadcast_command(client: Client, message: Message):
    await message.reply("**تم بدء نشر اعلان للبوت في جميع المجموعات، يرجى عدم تكرار الامر**")
    await send_message_to_chats()
    await message.reply("**تم الانتهاء من الاعلان في جميع المجموعات**")
