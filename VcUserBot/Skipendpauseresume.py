from pyrogram import Client, filters
from pyrogram.types import Message

from config import HNDLR, call_py
from VcUserBot.helpers.decorators import authorized_users_only
from VcUserBot.helpers.handlers import skip_current_song, skip_item
from VcUserBot.helpers.queues import QUEUE, clear_queue


@Client.on_message(filters.command(["skip"], prefixes=f"{HNDLR}"))
async def skip(client, m: Message):
    await m.delete()
    chat_id = m.chat.id
    if len(m.command) < 2:
        op = await skip_current_song(chat_id)
        if op == 0:
            await m.reply("**🙄لا يوجد شيء في قائمة الانتظار لتخطيه!**")
        elif op == 1:
            await m.reply("**😩قائمة انتظار فارغة ، مغادرة الدردشة الصوتية**")
        else:
            await m.reply(
                f"**⏭ تم التخطي** \n**🎧 الان يتم تشغيل** - [{op[0]}]({op[1]}) | `{op[2]}`",
                disable_web_page_preview=True,
            )
    else:
        تخطي= m.text.split(None, 1)[1]
        OP = "**🗑️ تمت إزالة الأغاني التالية من قائمة الانتظار: -**"
        if chat_id in QUEUE:
            items = [int(x) for x in skip.split(" ") if x.isdigit()]
            items.sort(reverse=True)
            for x in items:
                if x == 0:
                    pass
                else:
                    hm = await skip_item(chat_id, x)
                    if hm == 0:
                        pass
                    else:
                        OP = OP + "\n" + f"**#⃣{x}** - {hm}"
            await m.reply(OP)


@Client.on_message(filters.command(["انهاء"], prefixes=f"{HNDLR}"))
async def انهاء(client, m: Message):
    await m.delete()
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.leave_group_call(chat_id)
            clear_queue(chat_id)
            await m.reply("**😐تم الانهاء**")
        except Exception as e:
            await m.reply(f"**ERROR** \n`{e}`")
    else:
        await m.reply("**🤨مفيش حاجة شغالة إنت بتهزر !**")


@Client.on_message(filters.command(["ايقاف"], prefixes=f"{HNDLR}"))
async def ايقاف(client, m: Message):
    await m.delete()
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.pause_stream(chat_id)
            await m.reply(
                f"**⏸ تم ايقاف التشغيل.**\n\n• عشان تكمل التشغيل, اكتب كلمه» {HNDLR}استئناف"
            )
        except Exception as e:
            await m.reply(f"**ERROR** \n`{e}`")
    else:
        await m.reply("**🤨مفيش حاجة شغالة إنت بتهزر!**")


@Client.on_message(filters.command(["استئناف"], prefixes=f"{HNDLR}"))
async def استئناف(client, m: Message):
    await m.delete()
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.resume_stream(chat_id)
            await m.reply(
                f"**▶ تم الاستئناف**\n\n• عشان توقف التشغيل, اكتب كلمه» {HNDLR}ايقاف**"
            )
        except Exception as e:
            await m.reply(f"**ERROR** \n`{e}`")
    else:
        await m.reply("**🙄 مفيش حاجة واقفة أساسا أنت بتهزر!**")
