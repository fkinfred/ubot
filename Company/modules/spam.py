import asyncio

from pyrogram import filters

from Company import ubot
from Company.config import PREFIX
from Company.modules.bot import add_command_help

add_command_help(
    "spam",
    [
        ["spam <jumlah spam> <text>", "Mengirim teks secara spam dalam obrolan."],
        [
            "mspam <balas pesan>",
            "Untuk spam pesan yang di balas.",
        ],
        [
            "dspam",
            "Delay spam format ?dspam jumlah waktu pesan"
        ],
        [
            "delaystiker",
            "Delay spam media format ?delaystiker jumlah waktu balas media"
        ],
    ],
)


@ubot.on_message(filters.command("spam", PREFIX) & filters.me)
async def _(client, message):
    if message.reply_to_message:
        spam = await message.reply("Diproses")
        reply_id = message.reply_to_message.id
        quantity = int(message.text.split(None, 2)[1])
        spam_text = message.text.split(None, 2)[2]
        await asyncio.sleep(1)
        await message.delete()
        await spam.delete()
        for i in range(quantity):
            await client.send_message(
                message.chat.id, spam_text, reply_to_message_id=reply_id
            )
            await asyncio.sleep(0.1)
    else:
        if len(message.command) < 2:
            await message.reply_text("⚡ Usage:\n !spam jumlah spam, text spam")
        else:
            spam = await message.reply("Diproses")
            quantity = int(message.text.split(None, 2)[1])
            spam_text = message.text.split(None, 2)[2]
            await asyncio.sleep(1)
            await message.delete()
            await spam.delete()
            for i in range(quantity):
                await client.send_message(message.chat.id, spam_text)
                await asyncio.sleep(0.1)


@ubot.on_message(filters.command("mspam", PREFIX) & filters.me)
async def _(client, message):
    spam = message.reply_to_message
    if not spam and len(message.command) < 1:
        return await message.reply("contoh : !mspam 3 balas ke pesan")
    jumlah = message.command[1]
    for _ in range(int(jumlah)):
        await spam.copy(message.chat.id)
        await asyncio.sleep(1)
        
@ubot.on_message(filters.command("dspam", PREFIX) & filters.me)
async def delayspam(client, message):
    if len(message.command) < 4:
        return await message.reply("__Format salah silahkan seperti ?dspam waktu jumlah pesan\ncontoh : `?dspam 10 5 apa iya`")
    chat = message.chat.id
    xadega = "".join(message.text.split(maxsplit=1)[1:]).split(" ", 2)
    userbot = xadega[1:]
    waktu = float(xadega[0])
    jumlah = int(userbot[0])
    pesan = str(userbot[1])
    kk = await message.edit(f"Memulai delayspam jumlah pesan {jumlah} dengan waktu {waktu}")
    for _ in range(jumlah):
        await client.send_message(chat, pesan)
        await asyncio.sleep(waktu)
        await kk.delete()
            
    return await client.send_message(chat, f"Berhasil delayspam jumlah {jumlah} waktu {waktu}")
    
@ubot.on_message(filters.command("delaystiker", PREFIX) & filters.me)
async def _(client, message):
    spam = message.reply_to_message
    if not spam and len(message.command) < 2:
        return await message.reply("format : !delaystiker jumlah waktu \ncontoh : !delaystiker 3 5 balas ke pesan")
    jumlah = message.command[1]
    time = int(message.command[2])
    for _ in range(int(jumlah)):
        await spam.copy(message.chat.id)
        await asyncio.sleep(time)
