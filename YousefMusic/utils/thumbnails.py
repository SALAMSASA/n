import os
import re
import textwrap
import aiofiles
import aiohttp
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps
from youtubesearchpython.__future__ import VideosSearch
from YousefMusic import app
from config import YOUTUBE_IMG_URL
from config import OWNER_ID
import logging

# إعداد تسجيل الدخول
logging.basicConfig(level=logging.INFO)

def change_image_size_fill(max_width, max_height, image):
    return ImageOps.fit(image, (max_width, max_height), Image.LANCZOS)

def enhance_image(image):
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(0.5)  # زيادة التباين قليلاً
    enhancer = ImageEnhance.Sharpness(image)
    image = enhancer.enhance(2)  # زيادة الحدة
    return image

async def fetch_video_data(video_id):
    url = f"https://www.youtube.com/watch?v={video_id}"
    results = VideosSearch(url, limit=1)
    result = (await results.next())["result"][0]
    video_data = {
        "title": re.sub(r"\W+", " ", result.get("title", "Unsupported Title")).title(),
        "duration": result.get("duration", "Unknown Mins"),
        "thumbnail": result["thumbnails"][0]["url"].split("?")[0],
        "views": result["viewCount"].get("short", "Unknown Views"),
        "channel": result["channel"].get("name", "Unknown Channel")
    }
    return video_data

async def download_image(url, file_path):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                async with aiofiles.open(file_path, mode="wb") as f:
                    await f.write(await resp.read())

def overlay_text(draw, text, position, font, fill="white"):
    draw.text(
        position,
        text,
        fill=fill,
        font=font,
    )

async def get_owner_image():
    return "YousefMusic/assets/SALAM.png"

async def get_thumb(video_id):
    cache_path = f"cache/{video_id}.png"
    if os.path.isfile(cache_path):
        return cache_path

    try:
        video_data = await fetch_video_data(video_id)
        thumbnail_url = video_data["thumbnail"]
        temp_thumb_path = f"cache/thumb_{video_id}.png"
        
        await download_image(thumbnail_url, temp_thumb_path)
        owner_image_path = await get_owner_image()
        
        youtube_image = Image.open(temp_thumb_path)
        resized_image = change_image_size_fill(1280, 720, youtube_image).convert("RGBA")
        enhanced_image = enhance_image(resized_image)
        background = enhanced_image.filter(ImageFilter.BoxBlur(15))
        background = ImageEnhance.Brightness(background).enhance(0.6)
        
        owner_image = Image.open(owner_image_path)
        owner_image.thumbnail((500, 500), Image.LANCZOS)
        owner_image_with_border = ImageOps.expand(owner_image, border=15, fill="white")
        
        background.paste(owner_image_with_border, (50, 100), owner_image_with_border)  # لصق صورة المالك في المكان المرغوب مع قناة ألفا
        
        draw = ImageDraw.Draw(background)
        
        # تحميل الخط لكل النصوص
        font_path = "YousefMusic/assets/font2.ttf"  # المسار للخط
        font2_size = 30  # حجم الخط الجديد
        font2 = ImageFont.truetype(font_path, font2_size)  # خط جديد
        
        # وضع النص "SALAM PlAYiNg" بخط أكبر وحواف بيضاء
        text = "SALAM PlAYiNg"
        position = (600, 150)
        text_color = "white"
        outline_color = "white"
        outline_width = 1
        font_large = ImageFont.truetype(font_path, 70)  # حجم الخط الكبير
        draw.text(position, text, font=font_large, fill=text_color)
        draw.text((position[0] - outline_width, position[1]), text, font=font_large, fill=outline_color)
        draw.text((position[0] + outline_width, position[1]), text, font=font_large, fill=outline_color)
        draw.text((position[0], position[1] - outline_width), text, font=font_large, fill=outline_color)
        draw.text((position[0], position[1] + outline_width), text, font=font_large, fill=outline_color)
        
        # حساب العرض الأقصى للعنوان ليتناسب مع الصورة
        max_width_title = 550

        # وضع عنوان الفيديو بالخط الشائع
        title_lines = textwrap.wrap(video_data["title"], width=40)
        for i, line in enumerate(title_lines):
            overlay_text(draw, line, (600, 280 + 40 * i), font2)  # استخدام الخط الجديد
        
        # وضع المعلومات الإضافية (المشاهدات، المدة، القناة) بخط font2
        overlay_text(draw, f"Views : {video_data['views'][:23]}", (600, 450), font2)
        overlay_text(draw, f"Duration : {video_data['duration'][:23]} Mins", (600, 490), font2)
        overlay_text(draw, f"Channel : {video_data['channel']}", (600, 530), font2)
        
        os.remove(temp_thumb_path)
        background.save(cache_path)
        return cache_path
    except Exception as e:
        logging.error(f"Error in get_thumb: {e}")
        return YOUTUBE_IMG_URL
