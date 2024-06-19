import math
import os
import time
from asyncio import sleep

from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.errors import RPCError

from Company import bot, ubot
from Company.config import PREFIX
from Company.modules.bot import add_command_help
from Company.utils.data import *
from Company.utils.misc import get_arg

## original code kenkan

add_command_help(
    "dor",
    [
        [
            "dor [link]",
            "Untuk mengambil konten yang di anti teruskan.",
        ],
    ],
)


async def progress_dl(current, total, ud_type, message, start):
    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        # if round(current / total * 100, 0) % 5 == 0:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion

        elapsed_time = TimeFormatter(milliseconds=elapsed_time)
        estimated_total_time = TimeFormatter(milliseconds=estimated_total_time)

        progress = "[{0}{1}] \n**Progress**: {2}%\n".format(
            "".join(["●" for i in range(math.floor(percentage / 5))]),
            "".join(["○" for i in range(20 - math.floor(percentage / 5))]),
            round(percentage, 2),
        )

        tmp = progress + "{0} of {1}\n**Speed**: {2}/s\n**ETA**: {3}\n".format(
            humanbytes(current),
            humanbytes(total),
            humanbytes(speed),
            # elapsed_time if elapsed_time != '' else "0 s",
            estimated_total_time if estimated_total_time != "" else "0 s",
        )
        try:
            await message.edit(text="{}\n {}".format(ud_type, tmp))
        except:
            pass


def humanbytes(size):
    # https://stackoverflow.com/a/49361727/4723940
    # 2**10 = 1024
    if not size:
        return ""
    power = 2**10
    n = 0
    Dic_powerN = {0: " ", 1: "Ki", 2: "Mi", 3: "Gi", 4: "Ti"}
    while size > power:
        size /= power
        n += 1
    return str(round(size, 2)) + " " + Dic_powerN[n] + "B"


def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = (
        ((str(days) + "d, ") if days else "")
        + ((str(hours) + "h, ") if hours else "")
        + ((str(minutes) + "m, ") if minutes else "")
        + ((str(seconds) + "s, ") if seconds else "")
        + ((str(milliseconds) + "ms, ") if milliseconds else "")
    )
    return tmp[:-2]


@ubot.on_message(filters.me & filters.command("dor", PREFIX))
async def nyolongnih(client, message):
    link = get_arg(message)
    if not link:
        return await message.reply("Silahkan kombinasikan command dan link")
    au = await message.reply("Dor dulu cuy")
    c_time = time.time()
    if link.startswith("https"):
        if "?single" in link:
            link_ = link.split("?single")[0]
            msg_id = int(link_.split("/")[-1])
        else:
            msg_id = int(link.split("/")[-1])
        if "t.me/c/" in link:
            try:
                chat = int("-100" + str(link.split("/")[-2]))
                dia = await client.get_messages(chat, msg_id)
            except RPCError:
                await au.edit("Sepertinya ada yang salah")
            try:
                await client.copy_message(
                    message.chat.id, chat, msg_id, reply_to_message_id=message.id
                )
                await au.delete()
            except:
                await colong(client, message, dia, progress_dl, au, c_time)
            await au.delete()
        else:
            try:
                chat = str(link.split("/")[-2])
                hah = await client.get_chat(chat)
            except RPCError:
                await au.edit("Sepertinya ada yang salah")
            if hah.type == ChatType.CHANNEL:
                dia = await bot.get_messages(chat, msg_id)
                await client.unblock_user(bot.me.username)
                await dia.copy(message.from_user.id)
                await sleep(2)
                async for enak in client.get_chat_history(bot.me.username, 1):
                    await enak.copy(message.chat.id, reply_to_message_id=message.id)
                    await au.delete()
                    await enak.delete()
            else:
                try:
                    await client.copy_message(
                        message.chat.id, chat, msg_id, reply_to_message_id=message.id
                    )
                    await au.delete()
                except:
                    dia = await client.get_messages(chat, msg_id)
                    await colong(client, message, dia, progress_dl, au, c_time)
                    await au.delete()

    else:
        await au.edit("Sepertinya ada yang salah")


@ubot.on_message(filters.me & filters.command("dur", PREFIX))
async def curinih(client, message):
    dia = message.reply_to_message
    if not dia:
        return await message.reply("Silahkan balas ke pesan")
    anu = await client.download_media(dia)
    await message.delete()
    log = "me"
    if dia.photo:
        await client.send_photo(
            log, anu, caption=dia.caption, caption_entities=dia.caption_entities
        )
        os.remove(anu)
    elif dia.video:
        asu = await client.download_media(dia.video.thumbs[0].file_id)
        await client.send_video(
            log,
            anu,
            caption=dia.caption,
            caption_entities=dia.caption_entities,
            duration=dia.video.duration,
            thumb=asu,
        )
        os.remove(anu)
        os.remove(asu)


async def colong(client, message, dia, progress_dl, au, c_time):
    if dia.text:
        await dia.copy(message.chat.id, reply_to_message_id=message.id)
    if dia.sticker:
        await dia.copy(message.chat.id, reply_to_message_id=message.id)
    if dia.photo:
        anu = await client.download_media(dia)
        await client.send_photo(
            message.chat.id,
            anu,
            caption=dia.caption,
            caption_entities=dia.caption_entities,
            reply_to_message_id=message.id,
        )
        os.remove(anu)
    if dia.video:
        anu = await client.download_media(
            dia,
            progress=progress_dl,
            progress_args=("**Trying To Download...**", au, c_time),
        )
        asu = await client.download_media(dia.video.thumbs[0].file_id)
        await client.send_video(
            message.chat.id,
            anu,
            caption=dia.caption,
            caption_entities=dia.caption_entities,
            duration=dia.video.duration,
            width=dia.video.width,
            height=dia.video.height,
            thumb=asu,
            progress=progress_dl,
            progress_args=("**Trying To Uploading**", au, c_time),
            reply_to_message_id=message.id,
        )
        os.remove(anu)
        os.remove(asu)
    if dia.audio:
        anu = await client.download_media(
            dia,
            progress=progress_dl,
            progress_args=("**Trying To Download...**", au, c_time),
        )
        await client.send_audio(
            message.chat.id,
            anu,
            caption=dia.caption,
            caption_entities=dia.caption_entities,
            progress=progress_dl,
            progress_args=("**Trying To Uploading**", au, c_time),
            reply_to_message_id=message.id,
        )
        os.remove(anu)
    if dia.voice:
        anu = await client.download_media(
            dia,
            progress=progress_dl,
            progress_args=("** Trying To Download...**", au, c_time),
        )
        await client.send_voice(
            message.chat.id,
            anu,
            caption=dia.caption,
            caption_entities=dia.caption_entities,
            progress=progress_dl,
            progress_args=("**Trying To Uploading**", au, c_time),
            reply_to_message_id=message.id,
        )
        os.remove(anu)
    if dia.document:
        anu = await client.download_media(
            dia,
            progress=progress_dl,
            progress_args=("** Trying To Download...**", au, c_time),
        )
        await client.send_document(
            message.chat.id,
            anu,
            caption=dia.caption,
            caption_entities=dia.caption_entities,
            progress=progress_dl,
            progress_args=("**Trying To Uploading**", au, c_time),
            reply_to_message_id=message.id,
        )
        os.remove(anu)
    if dia.animation:
        await client.send_animation(
            message.chat.id,
            anu,
            caption=dia.caption,
            caption_entities=dia.caption_entities,
            reply_to_message_id=message.id,
        )
        os.remove(anu)
