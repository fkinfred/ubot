from pyrogram import filters

from Company import ubot
from Company.config import PREFIX
from Company.modules.bot import add_command_help
from Company.utils.data import *
from Company.utils.misc import *

add_command_help(
    "setting",
    [
        [
            "setlog",
            "Untuk menganti gc log.",
        ],
        [
            "setlogo [link photo]",
            "Untuk log help, link wajib dari telegra.ph.",
        ],
    ],
)


@ubot.on_message(filters.command("setlogo", PREFIX) & filters.me)
async def pm_loger(client, message):
    if client.me.id == ubot.me.id:
        return await message.reply(
            "Karena kamu userbot pertama tidak bisa menggunakan perintah ini"
        )
    anu = get_arg(message)
    if not anu:
        return await message.reply("Silahkan kombinasikan dengan link")
    iya = await cek_config(client.me.id)
    for i in iya:
        log = i["log"]
        pmlog = i["pmlog"]
        gruplog = i["gruplog"]
    if anu.endswith("jpg"):
        await add_config(client.me.id, anu, log, pmlog, gruplog)
        await message.reply(f"Logo berhasil di set {anu}")
    elif not anu.endswith("jpg"):
        await message.reply(f"{anu} Salah silahkan isi link dari telegra.ph")


@ubot.on_message(filters.command("setlog", PREFIX) & filters.me)
async def grup_loger(client, message):
    if client.me.id == ubot.me.id:
        return await message.reply(
            "Karena kamu userbot pertama tidak bisa menggunakan perintah ini"
        )
    anu = get_arg(message)
    if not anu:
        return await message.reply("Silahkan kombinasikan dengan on atau off")
    iya = await cek_config(client.me.id)
    for i in iya:
        logo = i["logo"]
        pmlog = i["pmlog"]
        gruplog = i["gruplog"]
    if anu.startswith(-100):
        await add_config(client.me.id, logo, anu, pmlog, gruplog)
        await message.reply(f"Log berhasil di set {anu}")
    elif not anu.startswith(-100):
        await message.reply(
            f"{anu} Salah silahkan isi id group berawalan -100 dan di wajibkan sudah join ke grup tersebut"
        )
