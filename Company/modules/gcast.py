import asyncio

import dotenv
from pyrogram import Client, enums, filters
from pyrogram.types import Message
from requests import get

from Company import SUDO, ubot
from Company.config import PREFIX, DEVS, BLACKLIST_CHAT
from Company.utils.misc import restart, get_arg, edit_or_reply
from Company.utils.data import add_black, all_black, black_info, del_black
from Company.modules.bot import add_command_help

add_command_help(
    "gcast",
    [
        [
            "gcast <text/reply>",
            "Mengirim Global Broadcast pesan ke Seluruh Grup yang kamu masuk. (Bisa Mengirim Media/Sticker)",
        ],
        [
            "gucast <text/reply>",
            "Mengirim Global Broadcast pesan ke Seluruh Private Massage / PC yang masuk. (Bisa Mengirim Media/Sticker)",
        ],
        [
            "blchat",
            "Untuk Mengecek informasi daftar blacklist gcast.",
        ],
        [
            "addbl",
            "Untuk Menambahkan grup tersebut ke blacklist gcast.",
        ],
        [
            "delbl",
            f"Untuk Menghapus grup tersebut dari blacklist gcast.\n\n  •  **Note : **Ketik perintah** `? addblacklist` **dan** `? delblacklist` **di grup yang kamu Blacklist.",
        ],
    ],
)


@ubot.on_message(filters.command("cgcast", ".") & filters.user(SUDO))
@ubot.on_message(filters.command("gcast", PREFIX) & filters.me)
async def gcast_cmd(client: Client, message: Message):
    if message.reply_to_message or get_arg(message):
        Man = await message.reply("`Started global broadcast...`")
    else:
        return await message.reply("**Berikan Sebuah Pesan atau Reply**")
    done = 0
    error = 0
    arrayBl = client._dialogue.get(client.me.id, [])
    async for dialog in client.get_dialogs():
        if dialog.chat.type in (enums.ChatType.GROUP, enums.ChatType.SUPERGROUP):
            if message.reply_to_message:
                msg = message.reply_to_message
            elif get_arg:
                msg = get_arg(message)
            chat = int(dialog.chat.id)
            if chat in BLACKLIST_CHAT:
                continue
            if chat in arrayBl:
                continue
            else:
                try:
                    if message.reply_to_message:
                        await msg.copy(chat)
                    elif get_arg:
                        await client.send_message(chat, msg)
                    done += 1
                    await asyncio.sleep(0.3)
                except Exception:
                    error += 1
                    await asyncio.sleep(0.3)
    await Man.edit(
        f"**Berhasil Mengirim Pesan Ke** `{done}` **Grup, Gagal Mengirim Pesan Ke** `{error}` **Grup**"
    )


@ubot.on_message(filters.command("gucast", PREFIX) & filters.me)
async def gucast_cmd(client: Client, message: Message):
    if message.reply_to_message or get_arg(message):
        Man = await edit_or_reply(message, "`Started global broadcast...`")
    else:
        return await message.edit_text("**Berikan Sebuah Pesan atau Reply**")
    done = 0
    error = 0
    async for dialog in client.get_dialogs():
        if dialog.chat.type == enums.ChatType.PRIVATE and not dialog.chat.is_verified:
            if message.reply_to_message:
                msg = message.reply_to_message
            elif get_arg:
                msg = get_arg(message)
            chat = dialog.chat.id
            if chat not in DEVS:
                try:
                    if message.reply_to_message:
                        await msg.copy(chat)
                    elif get_arg:
                        await client.send_message(chat, msg)
                    done += 1
                    await asyncio.sleep(0.3)
                except Exception:
                    error += 1
                    await asyncio.sleep(0.3)
    await Man.edit_text(
        f"**Berhasil Mengirim Pesan Ke** `{done}` **chat, Gagal Mengirim Pesan Ke** `{error}` **chat**"
    )


@ubot.on_message(filters.command("addbl", PREFIX) & filters.me)
async def blacklist(client: Client, message: Message):
    kay = await message.reply("<b>ᴛᴜɴɢɢᴜ sᴇʙᴇɴᴛᴀʀ . . .</b>")
    # if message.reply_to_message or get_arg(message):
    # else:
    #     return await message.edit_text("**Berikan Sebuah Format -100**")
    grup = message.chat.id
    title = message.chat.title
    existing = await black_info(client.me.id, grup)
    if existing:
        return await kay.edit('ChatId sudah berapa di Blacklist.')
    await add_black(client.me.id, grup, title)
    await kay.edit(f"**Ditambahkan ke dalam Blacklist Hahaha🐷 Gcast**\n`{grup} {title}`")


@ubot.on_message(filters.command("delbl", PREFIX) & filters.me)
async def ungblacker(client, message):
    # if message.reply_to_message or get_arg(message):
    kay = await message.reply("<b>ᴛᴜɴɢɢᴜ sᴇʙᴇɴᴛᴀʀ . . .</b>")
    chatId = message.chat.id
    await del_black(client.me.id, chatId)
    await kay.edit(f"**Dihapus dari Blacklist Gcast**\n`{id}`")


@ubot.on_message(filters.command("listbl", PREFIX) & filters.me)
async def chatbl(client: Client, message: Message):
    arrayBlGcast = await all_black(client.me.id)
    sd = "**• Daftar Blacklist Gcast**\n\n"
    num = 0
    if len(arrayBlGcast) == 0:
        return await message.reply('Grup Blacklist Masing Kosong.')
    for x in arrayBlGcast:
        num += 1
        sd += f'{num}. {x["title"]} [ {x["grup"]} ]\n'
    await message.reply(sd)
