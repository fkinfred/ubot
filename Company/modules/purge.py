import asyncio

from pyrogram import filters

from Company import ubot
from Company.config import OWNER_ID, PREFIX
from Company.modules.bot import add_command_help

add_command_help(
    "purge",
    [
        ["del", "Menghapus pesan, balas ke pesan."],
        ["purge", "Menghapus pesan, balas ke pesan."],
        ["purgeme [angka]", "Menghapus jumlah pesan anda, yang mau anda hapus."],
    ],
)


@ubot.on_message(filters.me & filters.command("del", PREFIX))
async def del_user(_, message):
    rep = message.reply_to_message
    await message.delete()
    await rep.delete()


@ubot.on_message(filters.user(OWNER_ID) & filters.command("cpurgeme", PREFIX))
@ubot.on_message(filters.me & filters.command("purgeme", PREFIX))
async def purge_me_func(client, message):
    if len(message.command) != 2:
        return await message.delete()
    n = (
        message.reply_to_message
        if message.reply_to_message
        else message.text.split(None, 1)[1].strip()
    )
    if not n.isnumeric():
        return await message.reply("Argumen Tidak Valid")
    n = int(n)
    if n < 1:
        return await message.reply("Butuh nomor >=1-999")
    chat_id = message.chat.id
    message_ids = [
        m.id
        async for m in client.search_messages(
            chat_id,
            from_user=int(message.from_user.id),
            limit=n,
        )
    ]
    if not message_ids:
        return await message.reply("Tidak ada pesan yang ditemukan.")
    to_delete = [message_ids[i : i + 999] for i in range(0, len(message_ids), 999)]
    for hundred_messages_or_less in to_delete:
        await client.delete_messages(
            chat_id=chat_id,
            message_ids=hundred_messages_or_less,
            revoke=True,
        )
        mmk = await message.reply(f"✅ {n} Pesan Telah Di Hapus")
        await asyncio.sleep(2)
        await mmk.delete()


@ubot.on_message(filters.me & filters.command("purge", PREFIX))
async def purgefunc(client, message):
    await message.delete()
    if not message.reply_to_message:
        return await message.reply_text("Membalas pesan untuk dibersihkan.")
    chat_id = message.chat.id
    message_ids = []
    for message_id in range(
        message.reply_to_message.id,
        message.id,
    ):
        message_ids.append(message_id)
        if len(message_ids) == 100:
            await client.delete_messages(
                chat_id=chat_id,
                message_ids=message_ids,
                revoke=True,
            )
            message_ids = []
    if len(message_ids) > 0:
        await client.delete_messages(
            chat_id=chat_id,
            message_ids=message_ids,
            revoke=True,
        )
