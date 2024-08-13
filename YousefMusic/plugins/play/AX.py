from pyrogram import filters, Client
from YousefMusic import app
import asyncio
import config
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.types import VideoChatEnded, Message
from pytgcalls import PyTgCalls, StreamType
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped
from YousefMusic.core.call import Zelzaly
from YousefMusic.utils.database import *
from pytgcalls.exceptions import (NoActiveGroupCall,TelegramServerError,AlreadyJoinedError)


@app.on_message(filters.regex("^منو بل تصال$"))
async def strcall(client, message):
    assistant = await group_assistant(Zelzaly, message.chat.id)
    try:
        await assistant.join_group_call(message.chat.id, AudioPiped("https://graph.org/file/217aac5f9cd2b05f7ba5a.mp4"), stream_type=StreamType().pulse_stream)
        text = "~ المتكلمين بالأتصال :\n\n"
        participants = await assistant.get_participants(message.chat.id)
        k = 0
        for participant in participants:
            info = participant
            if info.muted == False:
                mut = " يتكلم "
            else:
                mut = " مسكر  "
            user = await client.get_users(participant.user_id)
            k += 1
            text += f"{k} ~ {user.mention} {mut}\n"
        text += f"\n~ عددهم : {len(participants)}"  

        # إضافة زر شفاف في الأسفل
        inline_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(". 𝖠 ' 𝟣𝟣𝟣 .", url=config.SUPPORT_CHAT)],
        ])      

        await message.reply(f"{text}", reply_markup=inline_keyboard)
        await asyncio.sleep(7)
        await assistant.leave_group_call(message.chat.id)
    except NoActiveGroupCall:
        await message.reply(f"- ماكو شي مشتغل .")
    except TelegramServerError:
        await message.reply(f"- حدث خطأ .")
    except AlreadyJoinedError:
        text = "~ المتكلمين بالأتصال :\n\n"
        participants = await assistant.get_participants(message.chat.id)
        k = 0
        for participant in participants:
            info = participant
            if info.muted == False:
                mut = " يتكلم "
            else:
                mut = " مسكر "
            user = await client.get_users(participant.user_id)
            k += 1
            text += f"{k} ~ {user.mention} {mut}\n"
        text += f"\n~ عددهم : {len(participants)}"

        # إضافة زر شفاف في الأسفل
        inline_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(". 𝖠 ' 𝟣𝟣𝟣 .", url=config.SUPPORT_CHAT)],
        ])
        await message.reply(f"{text}", reply_markup=inline_keyboard)
