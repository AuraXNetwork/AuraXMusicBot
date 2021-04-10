import os
from os import path
import requests
import aiohttp
import youtube_dl
from pyrogram import Client
from pyrogram.types import Message, Voice
from youtube_search import YoutubeSearch
from callsmusic import callsmusic, queues

import converter
from downloaders import youtube

from config import BOT_NAME as bn, DURATION_LIMIT
from helpers.filters import command, other_filters
from helpers.decorators import errors
from helpers.errors import DurationLimitError
from helpers.gets import get_url, get_file_name
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

@Client.on_message(command("ytt") & other_filters)
@errors
async def play(_, message: Message):

    text = message.text.split(" ", 1)
    query = text[1]
    lel = await message.reply("Searching.... `{query}` on You Tube")
    sender_id = message.from_user.id
    user_id = message.from_user.id
    sender_name = message.from_user.first_name
    user_name = message.from_user.first_name
    text = message.text.split(" ", 1)
    query = text[1]
    rpk = "["+user_name+"](tg://user?id="+str(user_id)+")"

    query = ''
    for i in message.command[1:]:
        query += ' ' + str(i)
    print(query)
    await lel.edit("✯𝗔𝘂𝗿𝗮𝗫✯=🔄 Processing...")
    ydl_opts = {"format": "bestaudio[ext=m4a]"}
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        url = f"https://youtube.com{results[0]['url_suffix']}"
        #print(results)
        title = results[0]["title"][:40]       
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f'thumb{title}.jpg'
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, 'wb').write(thumb.content)


        duration = results[0]["duration"]
        url_suffix = results[0]["url_suffix"]
        views = results[0]["views"]

    except Exception as e:
        lel.edit(
            "✯𝗔𝘂𝗿𝗮𝗫✯=❌ Song not found.\n\nTry another song or maybe spell it properly."
        )
        print(str(e))
        return

    keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Watch On YouTube 🎬",
                        url=f"{url}")
                   
                ]
            ]
        )

    keyboard2 = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Watch On YouTube 🎬",
                        url=f"{url}")
                   
                ]
            ]
        )

    audio = (message.reply_to_message.audio or message.reply_to_message.voice) if message.reply_to_message else None

    if audio:
        await lel.edit_text("Lel")

    elif url:
        file_path = await converter.convert(youtube.download(url))
    else:
        return await lel.edit_text("✯𝗔𝘂𝗿𝗮𝗫✯=❗ You did not give me anything to play!")

    if message.chat.id in callsmusic.pytgcalls.active_calls:
        position = await queues.put(message.chat.id, file=file_path)
        await message.reply_photo(
        photo=thumb_name, 
        caption=f"✯𝗔𝘂𝗿𝗮𝗫✯=#️⃣ Queued at position {position}!",
        reply_markup=keyboard2)
        return await lel.delete()
    else:
        callsmusic.pytgcalls.join_group_call(message.chat.id, file_path)
        await message.reply_photo(
        photo=thumb_name,
        reply_markup=keyboard,
        caption="✯𝗔𝘂𝗿𝗮𝗫✯=▶️ Playing.... song requested by {} via [YouTube](https://t.me/AuraXSupport)".format(
        message.from_user.mention()
        ),
    )
        return await lel.delete()
