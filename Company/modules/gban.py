from asyncio import sleep

from pyrogram import filters

from Company import SUDO, ubot
from Company.config import *
from Company.modules.bot import add_command_help
from Company.utils.data import *
from Company.utils.misc import *

add_command_help(
    "gban",
    [
        [
            "gban [username atau reply]",
            "Untuk memblokir user dari semua grup yang anda adminin",
        ],
        [
            "ungban [username atau reply]",
            "Untuk menghapus blokir user dari semua grup yang anda adminin",
        ],
        ["gbanlist", "Untuk menampilkan daftar gbanned"],
    ],
)


@ubot.on_message(filters.command("cgban", ".") & filters.user(SUDO))
@ubot.on_message(filters.command("gban", PREFIX) & filters.me)
async def gban_cuk(c, m):
    target = m.command[1] if len(m.command) > 1 else m.reply_to_message.from_user.id if m.reply_to_message and m.reply_to_message.from_user else None
    if not target:
        return await m.reply(
            "__Silahkan balas ke user atau gunakan id atau username user__"
        )
    try:
        user = await c.get_users(target)
    except:
        return await m.reply("__Tidak menemukan user tersebut__")
    if user.id == c.me.id:
        return await m.reply("Lol")
    fullname = f"{user.first_name} {user.last_name or ''}"
    iso = ggl = 0
    msg = await m.reply("__Processing...__")
    async for dialog in c.get_dialogs():
        if dialog.chat.type in (enums.ChatType.SUPERGROUP, enums.ChatType.GROUP):
            try:
                await c.ban_chat_member(dialog.chat.id, user.id)
                iso += 1
                await sleep(1)
            except Exception:
                ggl += 1
                await sleep(1)
    await add_gban(c.me.id, user.id, fullname)
    return await msg.edit(
        f"**Global Banned**\n✅ **Berhasil** : {iso} Chat\n❌ **Gagal**: {ggl} Chat\n👾 **User**: {fullname}"
    )


@ubot.on_message(filters.command("ungban", PREFIX) & filters.me)
async def ungban_cuk(c, m):
    target = m.command[1] if len(m.command) > 1 else m.reply_to_message.from_user.id if m.reply_to_message and m.reply_to_message.from_user else None
    if not target:
        return await m.reply(
            "__Silahkan balas ke user atau gunakan id atau username user__"
        )
    try:
        user = await c.get_users(target)
    except:
        return await m.reply("__Tidak menemukan user tersebut__")
    if user.id == c.me.id:
        return await m.reply("Lol")
    fullname = f"{user.first_name} {user.last_name or ''}"
    iso = ggl = 0
    msg = await m.reply("__Processing...__")
    async for dialog in c.get_dialogs():
        if dialog.chat.type in (enums.ChatType.SUPERGROUP, enums.ChatType.GROUP):
            try:
                await c.unban_chat_member(dialog.chat.id, user.id)
                iso += 1
                await sleep(1)
            except Exception:
                ggl += 1
                await sleep(1)
    await del_gban(c.me.id, user.id)
    return await msg.edit(
        f"**Global Unbanned**\n✅ **Berhasil** : {iso} Chat\n❌ **Gagal**: {ggl} Chat\n👾 **User**: {fullname}"
    )


@ubot.on_message(filters.command("gbanlist", PREFIX) & filters.me)
async def gbanlist_cuk(c, m):
    msg = "**Daftar Global Banned**\n\n"
    anu = await all_gban(c.me.id)
    if anu is False:
        return await m.reply("**Belum ada daftar global banned**")
    d = 0
    for x in anu:
        try:
            ex = x["user"]
            ss = x["nama"]
            d += 1
        except:
            continue
        msg += f"{d}. {ex} | `{ss}`\n"
    await m.reply(msg)
