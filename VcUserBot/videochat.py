import asyncio
import random

from pyrogram import Client, filters
from pyrogram.types import Message
from pytgcalls import StreamType
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped
from pytgcalls.types.input_stream.quality import (
    HighQualityAudio,
    HighQualityVideo,
    LowQualityVideo,
    MediumQualityVideo,
)
from youtubesearchpython import VideosSearch

from config import HNDLR, bot, call_py
from VcUserBot.helpers.queues import QUEUE, add_to_queue, get_queue

BrayDan = [
    "https://telegra.ph/file/31ba8f339b582bba7c946.jpg",
    "https://telegra.ph/file/31ba8f339b582bba7c946.jpg",
    "https://telegra.ph/file/31ba8f339b582bba7c946.jpg",
    "https://telegra.ph/file/31ba8f339b582bba7c946.jpg",
    "https://telegra.ph/file/31ba8f339b582bba7c946.jpg",
    "https://telegra.ph/file/31ba8f339b582bba7c946.jpg",
    "https://telegra.ph/file/31ba8f339b582bba7c946.jpg",
    "https://telegra.ph/file/31ba8f339b582bba7c946.jpg",
    "https://telegra.ph/file/31ba8f339b582bba7c946.jpg",
    "https://telegra.ph/file/31ba8f339b582bba7c946.jpg",
    "https://telegra.ph/file/31ba8f339b582bba7c946.jpg",
]

IMAGE_THUMBNAIL = random.choice(BrayDan)

# music player


def ytsearch(query):
    try:
        search = VideosSearch(query, limit=1)
        for r in search.result()["result"]:
            ytid = r["id"]
            if len(r["title"]) > 34:
                songname = r["title"][:35] + "..."
            else:
                songname = r["title"]
            url = f"https://www.youtube.com/watch?v={ytid}"
        return [songname, url]
    except Exception as e:
        print(e)
        return 0


async def ytdl(link):
    proc = await asyncio.create_subprocess_exec(
        "yt-dlp",
        "-g",
        "-f",
        # CHANGE THIS BASED ON WHAT YOU WANT
        "bestaudio",
        f"{link}",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if stdout:
        return 1, stdout.decode().split("\n")[0]
    else:
        return 0, stderr.decode()


# video player
def ytsearch(query):
    try:
        search = VideosSearch(query, limit=1)
        for r in search.result()["result"]:
            ytid = r["id"]
            if len(r["title"]) > 34:
                songname = r["title"][:35] + "..."
            else:
                songname = r["title"]
            url = f"https://www.youtube.com/watch?v={ytid}"
        return [songname, url]
    except Exception as e:
        print(e)
        return 0


async def ytdl(link):
    proc = await asyncio.create_subprocess_exec(
        "yt-dlp",
        "-g",
        "-f",
        # CHANGE THIS BASED ON WHAT YOU WANT
        "best[height<=?720][width<=?1280]",
        f"{link}",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if stdout:
        return 1, stdout.decode().split("\n")[0]
    else:
        return 0, stderr.decode()


@Client.on_message(filters.command(["تشغيل"], prefixes=f"{HNDLR}"))
async def تشغيل(client, m: Message):
    replied = m.reply_to_message
    chat_id = m.chat.id
    m.chat.title
    if replied:
        if replied.audio or replied.voice:
            await m.delete()
            huehue = await replied.reply("*🍷♥️انتظر قليلا**")
            dl = await replied.download()
            link = replied.link
            if replied.audio:
                if replied.audio.title:
                    songname = replied.audio.title[:35] + "..."
                else:
                    songname = replied.audio.file_name[:35] + "..."
            elif replied.voice:
                songname = "Voice Note"
            if chat_id in QUEUE:
                pos = add_to_queue(chat_id, songname, dl, link, "Audio", 0)
                await huehue.delete()
                # await m.reply_to_message.delete()
                await m.reply_photo(
                    photo="https://telegra.ph/file/31ba8f339b582bba7c946.jpg",
                    caption=f"""
**#⃣ تم اضاقة الأغنية يبرو🍷♥️▪️الموضع {pos}
💥 اسم الأغنية : {songname}
📈 ايدي المحادثة : {chat_id}
🎶 تم طلب الأغنية من: {m.from_user.mention}**
""",
                )
            else:
                await call_py.join_group_call(
                    chat_id,
                    AudioPiped(
                        dl,
                    ),
                    stream_type=StreamType().pulse_stream,
                )
                add_to_queue(chat_id, songname, dl, link, "Audio", 0)
                await huehue.delete()
                # await m.reply_to_message.delete()
                await m.reply_photo(
                    photo="https://telegra.ph/file/31ba8f339b582bba7c946.jpg",
                    caption=f"""
**▶ تم تشغيل الأغنية
💥 اسم الأغنية: {songname}
📈 ايدي المحادثة: {chat_id}
🎶 تم طلب الأغنية من: {m.from_user.mention}**
""",
                )

    else:
        if len(m.command) < 2:
            await m.reply("الرد على ملف الصوت أو إعطاء شيء للبحث 🍷♥️")
        else:
            await m.delete()
            huehue = await m.reply("🔎 جاري البحث... ")
            query = m.text.split(None, 1)[1]
            search = ytsearch(query)
            if search == 0:
                await huehue.edit("`لم يتم العثور علي شئ من المطلوب 🙄💔`")
            else:
                songname = search[0]
                url = search[1]
                hm, ytlink = await ytdl(url)
                if hm == 0:
                    await huehue.edit(f"**YTDL ايرور ⚠️** \n\n`{ytlink}`")
                else:
                    if chat_id in QUEUE:
                        pos = add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                        await huehue.delete()
                        # await m.reply_to_message.delete()
                        await m.reply_photo(
                            photo=f"{IMAGE_THUMBNAIL}",
                            caption=f"""
**#⃣ تم اضافة الأغنية المطلوبه▪️الموضع{pos}
💥 اسم الأغنية: {songname}
📈 أيدي المحادثه: {chat_id}
🎶 تم طلب الأغنية من: {m.from_user.mention}**
""",
                        )
                    else:
                        try:
                            await call_py.join_group_call(
                                chat_id,
                                AudioPiped(
                                    ytlink,
                                ),
                                stream_type=StreamType().pulse_stream,
                            )
                            add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                            await huehue.delete()
                            # await m.reply_to_message.delete()
                            await m.reply_photo(
                                photo=f"{IMAGE_THUMBNAIL}",
                                caption=f"""
**▶ تم بدأ تشغيل الأغنية
💥 اسم الأغنية: {songname}
📈 أيدي المحادثة: {chat_id}
🎶 تم طلب المحادثة من: {m.from_user.mention}**
""",
                            )
                        except Exception as ep:
                            await huehue.edit(f"`{ep}`")


@Client.on_message(filters.command(["فيديو"], prefixes=f"{HNDLR}"))
async def فيديو(client, m: Message):
    replied = m.reply_to_message
    chat_id = m.chat.id
    m.chat.title
    if replied:
        if replied.video or replied.document:
            await m.delete()
            huehue = await replied.reply("**🗃️ يتم التحميل...")
            dl = await replied.download()
            link = replied.link
            if len(m.command) < 2:
                Q = 720
            else:
                pq = m.text.split(None, 1)[1]
                if pq == "720" or "480" or "360":
                    Q = int(pq)
                else:
                    Q = 720
                    await huehue.edit(
                        "`Only 720, 480, 360 Allowed` \n`Now Stream in 720p`"
                    )

            if replied.video:
                songname = replied.video.file_name[:35] + "..."
            elif replied.document:
                songname = replied.document.file_name[:35] + "..."

            if chat_id in QUEUE:
                pos = add_to_queue(chat_id, songname, dl, link, "Video", Q)
                await huehue.delete()
                # await m.reply_to_message.delete()
                await m.reply_photo(
                    photo="https://telegra.ph/file/31ba8f339b582bba7c946.jpg",
                    caption=f"""
**#⃣ تم اضافة الفيديو المطلوب▪️الموضع{pos}
💥 اسم الفيديو: {songname}
📈 ايدي المحادثة: {chat_id}
📹 تم طلب الفيديو من: {m.from_user.mention}**
""",
                )
            else:
                if Q == 720:
                    hmmm = HighQualityVideo()
                elif Q == 480:
                    hmmm = MediumQualityVideo()
                elif Q == 360:
                    hmmm = LowQualityVideo()
                await call_py.join_group_call(
                    chat_id,
                    AudioVideoPiped(dl, HighQualityAudio(), hmmm),
                    stream_type=StreamType().pulse_stream,
                )
                add_to_queue(chat_id, songname, dl, link, "Video", Q)
                await huehue.delete()
                # await m.reply_to_message.delete()
                await m.reply_photo(
                    photo="https://telegra.ph/file/31ba8f339b582bba7c946.jpg",
                    caption=f"""
**▶ تم بدأ تشغيل الفيديو 📹
💥 اسم الفيديو: {songname}
📈 أيدي المحادثة: {chat_id}
📹 تم طلب الفيديو من: {m.from_user.mention}**
""",
                )

    else:
        if len(m.command) < 2:
            await m.reply("**الرد على ملف الفيديو أو إعطاء شيء للبحث📹🍷♥️**")
        else:
            await m.delete()
            huehue = await m.reply("**🔎 يتم البحث...")
            query = m.text.split(None, 1)[1]
            search = ytsearch(query)
            Q = 720
            hmmm = HighQualityVideo()
            if search == 0:
                await huehue.edit(
                    "**Tidak Menemukan Apa pun untuk Kueri yang Diberikan**"
                )
            else:
                songname = search[0]
                url = search[1]
                hm, ytlink = await ytdl(url)
                if hm == 0:
                    await huehue.edit(f"**YTDL ايرور ⚠️** \n\n`{ytlink}`")
                else:
                    if chat_id in QUEUE:
                        pos = add_to_queue(chat_id, songname, ytlink, url, "Video", Q)
                        await huehue.delete()
                        # await m.reply_to_message.delete()
                        await m.reply_photo(
                            photo=f"{IMAGE_THUMBNAIL}",
                            caption=f"""
**#⃣ تم اضافة فيديو بنجاح▪️الموضع{pos}
💥 اسم الفيديو: {songname}
📈 أيدي المحادثة: {chat_id}
📹 تم طلب الفيديو من: {m.from_user.mention}**
""",
                        )
                    else:
                        try:
                            await call_py.join_group_call(
                                chat_id,
                                AudioVideoPiped(ytlink, HighQualityAudio(), hmmm),
                                stream_type=StreamType().pulse_stream,
                            )
                            add_to_queue(chat_id, songname, ytlink, url, "Video", Q)
                            await huehue.delete()
                            # await m.reply_to_message.delete()
                            await m.reply_photo(
                                photo=f"{IMAGE_THUMBNAIL}",
                                caption=f"""
**▶ تم بدأ تشغيل الفيديو📹💥
💥 أسم الفيديو: {songname}
📈 أيدي المحادثة: {chat_id}
📹 تم طلب الفيديو من: {m.from_user.mention}**
""",
                            )
                        except Exception as ep:
                            await huehue.edit(f"`{ep}`")


@Client.on_message(filters.command(["playfrom"], prefixes=f"{HNDLR}"))
async def playfrom(client, m: Message):
    chat_id = m.chat.id
    if len(m.command) < 2:
        await m.reply(
            f"**😹Use:** \n\n`{HNDLR}playfrom [chat_id/username]` \n`{HNDLR}playfrom [chat_id/username]`"
        )
    else:
        args = m.text.split(maxsplit=1)[1]
        if ";" in args:
            chat = args.split(";")[0]
            limit = int(args.split(";")[1])
        else:
            chat = args
            limit = 10
            lmt = 9
        await m.delete()
        hmm = await m.reply(f"🔎 Finding {limit} Random songs from {chat}**")
        try:
            async for x in bot.search_messages(chat, limit=limit, filter="audio"):
                location = await x.download()
                if x.audio.title:
                    songname = x.audio.title[:30] + "..."
                else:
                    songname = x.audio.file_name[:30] + "..."
                link = x.link
                if chat_id in QUEUE:
                    add_to_queue(chat_id, songname, location, link, "Audio", 0)
                else:
                    await call_py.join_group_call(
                        chat_id,
                        AudioPiped(location),
                        stream_type=StreamType().pulse_stream,
                    )
                    add_to_queue(chat_id, songname, location, link, "Audio", 0)
                    # await m.reply_to_message.delete()
                    await m.reply_photo(
                        photo="https://telegra.ph/file/6213d2673486beca02967.png",
                        caption=f"""
**▶ Start Playing Songs From {chat}
🏷️ Name: {songname}
💬 Chat ID: {chat_id}
🎧 Requested by: {m.from_user.mention}**
""",
                    )
            await hmm.delete()
            await m.reply(
                f"➕ Added {lmt} Song Into the Queue\n• Click {HNDLR}playlist To View Playlist**"
            )
        except Exception as e:
            await hmm.edit(f"**ERROR** \n`{e}`")


@Client.on_message(filters.command(["قائمه التشغيل", "القائمه"], prefixes=f"{HNDLR}"))
async def playlist(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        chat_queue = get_queue(chat_id)
        if len(chat_queue) == 1:
            await m.delete()
            await m.reply(
                f"**🎧 حاليا يتم التشغيل:** \n[{chat_queue[0][0]}]({chat_queue[0][2]}) | `{chat_queue[0][3]}`",
                disable_web_page_preview=True,
            )
        else:
            QUE = f"**🎧 حاليا يتم التشغيل:** \n[{chat_queue[0][0]}]({chat_queue[0][2]}) | `{chat_queue[0][3]}` \n\n**⏯ QUEUE LIST:**"
            l = len(chat_queue)
            for x in range(1, l):
                hmm = chat_queue[x][0]
                hmmm = chat_queue[x][2]
                hmmmm = chat_queue[x][3]
                QUE = QUE + "\n" + f"**#{x}** - [{hmm}]({hmmm}) | `{hmmmm}`\n"
            await m.reply(QUE, disable_web_page_preview=True)
    else:
        await m.reply("**🚫 لا يتم تشغيل اي شئ حاليا**")
