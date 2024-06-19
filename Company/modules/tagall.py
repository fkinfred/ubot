from asyncio import sleep

from pyrogram import Client, filters
from pyrogram.types import Message

from Company import ubot
from Company.config import PREFIX
from Company.utils.misc import get_arg
from Company.modules.bot import add_command_help

spam_chats = []


@ubot.on_message(filters.command("tagall", PREFIX) & filters.me)
async def mentionall(client: Client, message: Message):
    chat_id = message.chat.id
    direp = message.reply_to_message
    args = get_arg(message)
    if not direp and not args:
        return await message.edit("**Berikan saya pesan atau balas ke pesan!**")
    await message.delete()
    spam_chats.append(chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.get_chat_members(chat_id):
        if not chat_id in spam_chats:
            break
        usrnum += 1
        usrtxt += f"[{usr.user.first_name}](tg://user?id={usr.user.id}), "
        if usrnum == 5:
            if args:
                txt = f"{args}\n{usrtxt}"
                await client.send_message(chat_id, txt)
            elif direp:
                await direp.reply(usrtxt)
            await sleep(2)
            usrnum = 0
            usrtxt = ""
    try:
        spam_chats.remove(chat_id)
    except:
        pass


@ubot.on_message(filters.command("cancel", PREFIX) & filters.me)
async def cancel_spam(client: Client, message: Message):
    if not message.chat.id in spam_chats:
        return await message.edit("**Sepertinya tidak ada tagall disini.**")
    else:
        try:
            spam_chats.remove(message.chat.id)
        except:
            pass
        return await message.edit("**Memberhentikan Mention.**")


add_command_help(
    "tagall",
    [
        [
            "tagall [text/reply ke chat]",
            "Untuk Mention semua member group",
        ],
        [
            "cancel",
            f"Untuk Membatalkan Perintah .tagall",
        ],
    ],
)
