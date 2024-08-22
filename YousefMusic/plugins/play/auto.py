import random
import string
import asyncio
from pyrogram import Client, filters, enums
from pyrogram.errors import ChannelInvalid, ChatAdminRequired, ChatWriteForbidden, PeerIdInvalid
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, InputMediaPhoto
from config import START_IMG_URL
import config
from YousefMusic import Apple, Resso, SoundCloud, Spotify, Telegram, YouTube, app

from YousefMusic.utils.database import get_served_chats, remove_served_chat  # استيراد دالة إزالة القنوات

from config import BANNED_USERS, lyrical, CHANNEL_SUDO, YAFA_NAME, YAFA_CHANNEL

from YousefMusic.misc import SUDOERS

MESSAGE = f"""- - افضل بوت تشغيل اغاني وتحميلها في التلجرام ✨

يعمل في القنوات والمجموعات بدون توقف نهائيا 🎗.

اضف البوت الى مجموعتك او قناتك واستمتع
مع افضل بوت تشغيل اغاني في التلجرام
بدون اعلانات مزعجة او توقف على سورس ليثون🎻

معرف البوت 🎸 [ @{app.username} ]

➤ A BOT TO PLAY HIGH-QUALITY SONGS IN VOICE CHAT ♩🎸 \n\n-𝙱𝙾𝚃 ➤ @{app.username}"""

BUTTON = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("اضف البوت الي مجموعتك او قناتك ❤️✨", url=f"https://t.me/{app.username}?startgroup=True")
        ]
    ]
)

async def send_message_to_chats():
    try:
        chats = await get_served_chats()
        for chat_info in chats:
            chat_id = chat_info.get('chat_id')
            if isinstance(chat_id, int):
                try:
                    # إرسال الرسالة إلى الكروب أو القناة
                    await app.send_photo(chat_id, photo=START_IMG_URL, caption=MESSAGE, reply_markup=BUTTON)
                    await asyncio.sleep(3)
                except ChatAdminRequired:
                    print(f"Bot lacks admin rights in chat {chat_id}. Skipping...")
                except (ChannelInvalid, PeerIdInvalid):
                    print(f"Invalid chat ID {chat_id}. Skipping...")
                    # إزالة القناة غير الصالحة من قاعدة البيانات
                    await remove_served_chat(chat_id)
                except ChatWriteForbidden:
                    print(f"Bot is not allowed to send messages in chat {chat_id}. Skipping...")
                except Exception as e:
                    print(f"An unexpected error occurred in chat {chat_id}: {e}")
    except Exception as e:
        print(f"Failed to retrieve chats: {e}")

@app.on_message(filters.command(["اعلان للبوت"], ""))
async def auto_broadcast_command(client: Client, message: Message):
    await message.reply("تم بدء نشر اعلان للبوت في جميع القنوات والمجموعات، يرجى عدم تكرار الامر")
    await send_message_to_chats()
    await message.reply("تم الانتهاء من الاعلان في جميع القنوات والمجموعات")
