import os, asyncio
from typing import Optional
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from telegraph import upload_file
from YousefMusic import app

#---------------FUNCTION---------------#

def get_file_id(msg: Message) -> Optional[Message]:
    if not msg.media:
        return None

    for message_type in ("photo", "animation", "audio", "document", "video", "video_note", "voice", "sticker"):
        obj = getattr(msg, message_type)
        if obj:
            setattr(obj, "message_type", message_type)
            return obj

#---------------FUNCTION---------------#

@app.on_message(filters.command(["تليجراف", "تلكراف", "تلجراف", "تلغراف"], prefixes=""))
async def telegraph_upload(bot, update):
    replied = update.reply_to_message
    if not replied:
        return await update.reply_text("اعمل ريبلاي على صورة أو فيديو أقل من 5 ميجا")
    file_info = get_file_id(replied)
    if not file_info:
        return await update.reply_text("التنسيق لا يدعمه!")
    text = await update.reply_text(text="<code>التحميل على الخادم الخاص بي ...</code>", disable_web_page_preview=True)   
    media = await update.reply_to_message.download()   
    await text.edit_text(text="<code>اكتمل التنزيل. الآن أقوم بالتحميل على رابط تليجراف...</code>", disable_web_page_preview=True)                                            
    try:
        response = upload_file(media)
    except Exception as error:
        print(error)
        await text.edit_text(text=f"Error :- {error}", disable_web_page_preview=True)       
        return    
    try:
        os.remove(media)
    except Exception as error:
        print(error)
        return    
    await text.edit_text(
        text=f"↢ إليك رابط التليجراف الذي تم إنشاؤه 🫧 :-</b>\n\n<code>https://te.legra.ph{response[0]}</code>",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup( [[
            InlineKeyboardButton(text="‹ 𝖮𝗉𝖾𝗇 ›", url=f"https://te.legra.ph{response[0]}"),
            InlineKeyboardButton(text="‹ 𝖲𝗁𝖺𝗋𝖾 ›", url=f"https://telegram.me/share/url?url=https://te.legra.ph{response[0]}")
            ],[
            InlineKeyboardButton(text="‹ 𝖢𝗅𝗈𝗌𝖾 ›", callback_data="close")
            ]])
        )
