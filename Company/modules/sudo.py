from pyrogram import Client, filters
from pyrogram.types import Message 
import os
import sys

from Company.utils.misc import extract_user
from Company.utils.data import add_sudo, get_sudo, remove_sudo
from Company import ubot, SUDO
from Company.modules.bot import add_command_help 
from Company.config import PREFIX


def restart():
    os.execvp(sys.executable, [sys.executable, "-m", "Company"])


@ubot.on_message(filters.command("addsudo", PREFIX) & filters.me)
async def addSudo(client, message):
    msg = await message.reply("<b>sᴇᴅᴀɴɢ ᴍᴇᴍᴘʀᴏsᴇs...</b>")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(
            f"<b><code>{message.text}</code> ᴜsᴇʀ_ɪᴅ/ᴜsᴇʀɴᴀᴍᴇ</b>"
        )
    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)

    sudo_users = await get_sudo()
    if user_id in sudo_users:
        return await msg.edit(
            f"<b>[{user.first_name} {user.last_name or ''}](tg://user?id={user.id}) Sudah Dalam Daftar Sudo.</b>"
        )
    try:
        await add_sudo(user_id)
        SUDO.append(user_id)
        await msg.edit(
            f"<b>[{user.first_name} {user.last_name or ''}](tg://user?id={user.id}) Ditambahkan Ke Daftar Sudo.</b>"
        )
        return await restart()
    except Exception as error:
        return await msg.edit(error)


@ubot.on_message(filters.command("rmsudo", PREFIX) & filters.me)
async def listSudo(client, message):
    msg = await message.reply("<b>sᴇᴅᴀɴɢ ᴍᴇᴍᴘʀᴏsᴇs...</b>")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(
            f"<b><code>{message.text}</code> ᴜsᴇʀ_ɪᴅ/ᴜsᴇʀɴᴀᴍᴇ</b>"
        )
    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)

    sudo_users = await get_sudo()
    if user_id not in sudo_users:
        return await msg.edit(
            f"<b>[{user.first_name} {user.last_name or ''}](tg://user?id={user.id}) Tidak Ada Di Daftar Sudo.</b>"
        )
    try:
        await remove_sudo(user_id)
        SUDO.remove(user_id)
        await msg.edit(
            f"<b>[{user.first_name} {user.last_name or ''}](tg://user?id={user.id}) Dihapus Dari Daftar Sudo.</b>"
        )
        return await restart()
    except Exception as error:
        return await msg.edit(error)


@ubot.on_message(filters.command("listsudo", PREFIX) & filters.me)
async def removeSudo(client, message):
    sudoer = await get_sudo()
    caption = '<b>Daftar Pengguna Sudo</b>\n\n'
    if len(sudoer) == 0:
        return await message.reply('<b>Belum memiliki pengguna sudo.</b>')
    for x in sudoer:
        caption += f'- {x}\n'
    await message.reply(caption)


add_command_help(
    "sudo",
    [
        [f".addsudo <reply/berikan id>", "menambahkan sudo user."],
        [f".rmsudo", "menghapus sudo user."],
        [f".listsudo", "melihat daftar sudo user."],
    ],
)
