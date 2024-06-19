from asyncio import sleep

from pyrogram import filters
from pyrogram.errors import YouBlockedUser

from Company import ubot
from Company.config import PREFIX
from Company.modules.bot import add_command_help
from Company.utils.misc import *

add_command_help(
    "other",
    [
        [
            "sg <reply/userid/username>",
            "Untuk Mendapatkan Riwayat Nama Pengguna selama di telegram.",
        ],
        ["limit", "Cek akun telegram mu di batasi atau tidak"],
        ["q atau q [color]", "Membuat sticker dari text"],
    ],
)


@ubot.on_message(filters.me & filters.command("sg", PREFIX))
async def sangmata(c, m):
    user_id = await extract_user(m)
    if not user_id:
        return await m.reply("Silahkan balas atau kombinasikan dengan id atau username")
    sg_i = await m.reply("**🔍 Sedang Memeriksa**")
    await c.unblock_user("@SangMata_beta_bot")
    sg_m = await c.send_message("@SangMata_beta_bot", f"{user_id}")
    await sg_m.delete()
    await sleep(3)
    async for msg in c.get_chat_history("@SangMata_beta_bot", limit=4):
        await msg.copy(m.chat.id, reply_to_message_id=m.id)
        await msg.delete()
        await sg_i.delete()


@ubot.on_message(filters.me & filters.command("limit", PREFIX))
async def akunlimit(client, message):
    await client.unblock_user("SpamBot")
    anu = await client.send_message("SpamBot", "/start")
    await anu.delete()
    await sleep(2)
    async for jembut in client.get_chat_history("SpamBot", limit=1):
        wait_msg = await message.reply("Processing . . .")
        await wait_msg.edit(f"~ {jembut.text}")
        await jembut.delete()


@ubot.on_message(filters.command("q", PREFIX) & filters.me)
async def quotly(client, message):
    memek = get_arg(message)
    if not message.reply_to_message and not memek:
        await message.reply("Mohon balas ke pesan")
        return
    bot = "QuotLyBot"
    iya = await message.reply("Processing...")
    if message.reply_to_message:
        try:
            await message.reply_to_message.forward(bot)
        except YouBlockedUser:
            await client.unblock_user(bot)
            await message.reply_to_message.forward(bot)

        await sleep(6)
        async for pepek in client.search_messages(bot, limit=1):
            if pepek:
                await iya.delete()
                await pepek.copy(
                    message.chat.id,
                    reply_to_message_id=message.reply_to_message.id
                    if message.reply_to_message
                    else None,
                )
            else:
                return await iya.edit("Sepertinya ada yang salah")
    elif memek:
        anu = await client.send_message(bot, f"/qcolor {memek}")
        await anu.delete()
        await sleep(2)
        async for ppk in client.search_messages(bot, limit=1):
            await iya.edit(ppk.text)
            await ppk.delete()
