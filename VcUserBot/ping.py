import os
import sys
from datetime import datetime
from time import time

from pyrogram import Client, filters
from pyrogram.types import Message

from config import HNDLR, SUDO_USERS

# System Uptime
START_TIME = datetime.utcnow()
TIME_DURATION_UNITS = (
    ('Week', 60 * 60 * 24 * 7),
    ('Day', 60 * 60 * 24),
    ('Hour', 60 * 60),
    ('Min', 60),
    ('Sec', 1)
)

async def _human_time_duration(seconds):
    if seconds == 0:
        return "inf"
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append("{} {}{}".format(amount, unit, "" if amount == 1 else ""))
    return ", ".join(parts)


@Client.on_message(filters.command(["بنج"], prefixes=f"{HNDLR}"))
async def ping(client, m: Message):
    start = time()
    current_time = datetime.utcnow()
    m_reply = await m.reply_text("⚡")
    delta_ping = time() - start
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await m_reply.edit(
        f"<b>أنا أعمل بنجاح🍀</b> `{delta_ping * 1000:.3f} ms` \n<b>⏳مدة التشغيل</b> - `{uptime}`"
    )


@Client.on_message(
    filters.user(SUDO_USERS) & filters.command(["restart"], prefixes=f"{HNDLR}")
)
async def restart(client, m: Message):
    await m.delete()
    loli = await m.reply("1")
    await loli.edit("2")
    await loli.edit("3")
    await loli.edit("4")
    await loli.edit("5")
    await loli.edit("6")
    await loli.edit("7")
    await loli.edit("8")
    await loli.edit("9")
    await loli.edit("**🖥️SMSM-SOURCE🖱️تم تحديث الاكك بنجاح⌨️**")
    os.execl(sys.executable, sys.executable, *sys.argv)
    quit()


@Client.on_message(filters.command(["Good morning", "Gud morning", "gud mrng", "ഗുഡ് മോർണിംഗ്"], prefixes=f"{HNDLR}"))
async def goodmorning(client, m: Message):
    GM = f"""
<i>🍂☕️Gøød Mørning..⏱️ Have a nice day..🙂</i>
"""
    await m.reply(GM)


@Client.on_message(filters.command(["Good Evening", "Gud evng", "gud evening", "ഗുഡ് ഈവനിംഗ്", "ഗുഡ് ഈവെനിംഗ്"], prefixes=f"{HNDLR}"))
async def goodevening(client, m: Message):
    GE = f"""
<i> 😁Gøød Evening..☕️</i>
"""
    await m.reply(GE)


@Client.on_message(filters.command(["Good Night", "Gud nt", "gud night", "ഗുഡ് നൈറ്റ്‌", "gudnyt"], prefixes=f"{HNDLR}"))
async def goodnight(client, m: Message):
    GN = f"""
<i> 😴🛌Gøød Night 🌚</i>
"""
    await m.reply(GN)


@Client.on_message(filters.command(["سورس"], prefixes=f"{HNDLR}"))
async def سورس(client, m: Message):
    GN = f"""
<i> ⩹━━━━✗🍷𝑺𝑴𝑺𝑴 𝑺𝑶𝑼𝑹𝑪𝑬🍷✗━━━━⩺
DEV: @DEV_SMSM </i>
"""
    await m.reply(GN)
