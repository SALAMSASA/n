from pyrogram import enums
from pyrogram import types
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from YousefMusic import app

# قائمة لتخزين الهمسات المرسلة
hmses = {}

# دالة للرد برابط الهمسة
@app.on_message(filters.reply & (filters.regex("همسه") | filters.regex("اهمس")) & filters.group)
async def reply_with_link(client, message):
    user_id = message.reply_to_message.from_user.id
    my_id = message.from_user.id
    bar_id = message.chat.id
    start_link = f"https://t.me/{(await app.get_me()).username}?start=hms{my_id}to{user_id}in{bar_id}"
    reply_markup = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("‹ اضغط لارسال الهمسة 🍀 ›", url=start_link)]
        ]
    )
    await message.reply_text("‹ اضغط لارسال الهمسة 🍀 ›", reply_markup=reply_markup)

# متغير للتحقق مما إذا كان يتم انتظار الهمسة
waiting_for_hms = False

# دالة لبدء إرسال الهمسة
@app.on_message(filters.command("start"), group=89)
async def hms_start(client, message):
    if message.text.split(" ", 1)[-1].startswith("hms"):
        global waiting_for_hms, hms_ids
        hms_ids = message.text
        waiting_for_hms = True
        await message.reply_text(
            "- ارسل الهمسه الآن . ",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("‹ الغاء الهمسه ›", callback_data="hms_cancel")]]
            ),
        )

# دالة لإرسال الهمسة
@app.on_message(filters.private & filters.text & ~filters.command("start"), group=88)
async def send_hms(client, message):
    global waiting_for_hms
    if waiting_for_hms:
        to_id = int(hms_ids.split("to")[-1].split("in")[0])
        from_id = int(hms_ids.split("hms")[-1].split("to")[0])
        in_id = int(hms_ids.split("in")[-1])
        to_url = f"tg://openmessage?user_id={to_id}"
        from_url = f"tg://openmessage?user_id={from_id}"
        
        # تخزين الهمسة في القائمة
        hmses[str(to_id)] = {"hms": message.text, "bar": in_id}
        
        await message.reply_text("- تم ارسال الهمسة ⋅")
        
        # إرسال رسالة إشعار للمستقبل بأنه تم استلام همسة جديدة
        await app.send_message(
    chat_id=in_id,
    text=f"⌯ وصلتك همسة من »\n⦗ [{(await app.get_chat(from_id)).first_name}](tg://openmessage?user_id={from_id}) ⦘ 🍀⋅",
    reply_markup=InlineKeyboardMarkup(
        [
            [
                    InlineKeyboardButton("‹ اضغط لرؤية الهمسه 🍀 ›", callback_data="hms_answer"),
                ],[
                    InlineKeyboardButton(
                        "‹ 𝖲𝗈𝖴𝗋𝖼𝖾 𝐋𝐄𝐓 ›", url=f"https://t.me/ll0llld"),
            ]
        ]                   

         ),parse_mode=enums.ParseMode.MARKDOWN)
        
        waiting_for_hms = False
     
# دالة للتعامل مع الاستجابة لرؤية الهمسة
@app.on_callback_query(filters.regex("hms_answer"))
async def display_hms(client, callback):
    print("Inside display_hms function")
    in_id = callback.message.chat.id
    who_id = callback.from_user.id
    
    print(f"Callback from user ID: {who_id}")
    print(f"Callback message chat ID: {in_id}")

    if hmses.get(str(who_id)) is not None:
        print("Found whisper for this user")
        if hmses.get(str(who_id))["bar"] == in_id:
            print("Before answering callback")
            await callback.answer(hmses.get(str(who_id))["hms"], show_alert=True)
            print("After answering callback")
            # إرسال رسالة إشعار للمرسل بأن الهمسة قد فُتحت
            sender_id = int(hmses.get(str(who_id))["hms"].split("from")[-1])
            recipient_name = (await app.get_chat(callback.from_user.id)).first_name
            await app.send_message(sender_id, f"تم فتح الهمسة من قبل المستلم {recipient_name}.")
            print("Message sent to sender")
        else:
            print("The whisper is not for this chat")
    else:
        print("No whisper found for this user")
        await callback.answer("الهمسه ليست لك ⋅", show_alert=True)
        # إرسال رسالة إشعار للمرسل بأن الهمسة ليست له
        sender_id = int(hmses.get(str(who_id))["hms"].split("from")[-1])
        recipient_name = (await app.get_chat(callback.from_user.id)).first_name
        await app.send_message(sender_id, f"حاول المستخدم ({recipient_name}) الوصول")
