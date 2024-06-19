from pyrogram import filters

from Company import ubot
from Company.config import PREFIX
from Company.modules.bot import add_command_help
from Company.utils.data import *
from Company.utils.misc import get_arg

add_command_help(
    "notes",
    [
        [
            "save [nama dan balas ke pesan]",
            "Untuk menyimpan catatan.",
        ],
        [
            "get [nama]",
            "Untuk memanggil catatan.",
        ],
        [
            "dellnote [nama]",
            "Untuk menghapus catatan.",
        ],
        [
            "notes",
            "Untuk menampilkan daftar catatan.",
        ],
    ],
)


@ubot.on_message(filters.command("save", PREFIX) & filters.me)
async def simpan_notes(client, message):
    note_name = get_arg(message)
    user_id = message.from_user.id
    if not note_name:
        await message.reply("__Tolong berikan nama note__")
        return
    if not message.reply_to_message:
        await message.reply("__Tolong balas ke pesan__")
        return
    msg = message.reply_to_message
    iya = await log_info(user_id)
    log = "me" if iya is None else iya
    msgku = await msg.copy(log)
    await add_note(note_name, user_id, msgku.id)
    await message.reply(f"**Berhasil menyimpan note** `{note_name}`")


@ubot.on_message(filters.command("dellnote", PREFIX) & filters.me)
async def clear_notes(client, message):
    note_name = get_arg(message)
    user_id = message.from_user.id
    if not note_name:
        await message.reply("__Tolong berikan nama note__")
        return
    if not await note_info(note_name, user_id):
        await message.reply(f"__Tidak Ditemukan dalam database {note_name}__")
        return
    await del_note(note_name, user_id)
    await message.reply(f"__Catatan {note_name} Berhasil dihapus!__")


@ubot.on_message(filters.command("get", PREFIX) & filters.me)
async def lmao_note(client, message):
    user_id = message.from_user.id
    if not await all_note(user_id):
        return
    owo = get_arg(message)
    iya = await log_info(user_id)
    log = "me" if iya is None else iya
    if owo is None:
        return
    if await note_info(owo, user_id):
        sed = await note_info(owo, user_id)
        ea = await client.get_messages(log, sed["note_id"])

        await ea.copy(message.chat.id, reply_to_message_id=message.id)


@ubot.on_message(filters.command("notes", PREFIX) & filters.me)
async def noteses_ku(client, message):
    user_id = message.from_user.id
    poppy = await all_note(user_id)
    if poppy is False:
        await message.reply("**Belum ada catatan tersimpan**")
        return
    msg = "**Daftar catatan**\n"
    for iya in poppy:
        ppk = iya["note_name"]
        msg += f"**~** `{ppk}`\n"
    await message.reply(msg)
