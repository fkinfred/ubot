import asyncio

from pyrogram import filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import ChatPermissions, ChatPrivileges, Message

from Company import ubot
from Company.config import OWNER_ID, PREFIX
from Company.modules.bot import add_command_help
from Company.utils.misc import *

add_command_help(
    "admin",
    [
        ["ban <reply/username/userid>", "Membanned member dari grup."],
        ["unban <reply/username/userid>", "Membuka banned member dari grup."],
        ["kick <reply/username/userid>", "Mengeluarkan pengguna dari grup."],
        ["mute <reply/username/userid>", "Membisukan member dari Grup."],
        ["unmute <reply/username/userid>", "Membuka mute member dari Grup."],
        ["promote", "Mempromosikan member sebagai admin."],
        ["fullpromote", "Mempromosikan member sebagai cofounder."],
        ["demote", "Menurunkan admin sebagai member."],
        ["settitle", "Menerapkan title ke admin group."],
        ["invite", "mengundang pengguna lain ke dalam grup"],
        ["pin [balas ke pesan]", "Untuk memasang sematan pesan."],
        ["unpin [balas ke pesan]", "Untuk melepas sematan pesan."],
    ],
)


@ubot.on_message(
    filters.command(["kick", "ban", "mute", "unmute", "unban"], PREFIX)
    & filters.group
    & filters.me
)
async def _(client, message: Message):
    if message.command[0] == "kick":
        if message.reply_to_message:
            _id = message.reply_to_message.from_user.id
        else:
            if len(message.command) < 2:
                return await message.reply_text(
                    "Saya tidak dapat menemukan pengguna itu."
                )
            else:
                _id = message.text.split()[1]
        user_id = (await client.get_users(_id)).id
        if user_id == client.me.id:
            return await message.reply_text(
                "Aku tidak bisa menendang diriku sendiri, aku bisa pergi jika kamu mau."
            )
        if user_id in OWNER_ID:
            return await message.reply_text("Anda Tidak Bisa Menendang Anggota Ini")
        user = await message.chat.get_member(user_id)
        if user.status == ChatMemberStatus.ADMINISTRATOR:
            return await message.reply_text(
                "Saya tidak bisa menendang admin, Anda tahu aturannya, saya juga."
            )
        mention = (await client.get_users(user_id)).mention
        msg = f"**👤 Ditendang:** {mention}\n**👑 Admin:** {message.from_user.mention}"
        await message.chat.ban_member(user_id)
        await message.reply(msg)
        await asyncio.sleep(1)
        await message.chat.unban_member(user_id)
    elif message.command[0] == "ban":
        if message.reply_to_message:
            _id = message.reply_to_message.from_user.id
        else:
            if len(message.command) < 2:
                return await message.reply_text(
                    "Saya tidak dapat menemukan pengguna itu."
                )
            else:
                _id = message.text.split()[1]
        user_id = (await client.get_users(_id)).id
        if user_id == client.me.id:
            return await message.reply_text(
                "Aku tidak bisa membanned diriku sendiri, aku bisa pergi jika kamu mau."
            )
        if user_id in OWNER_ID:
            return await message.reply_text("Anda Tidak Bisa Membanned Anggota Ini")
        user = await message.chat.get_member(user_id)
        if user.status == ChatMemberStatus.ADMINISTRATOR:
            return await message.reply_text(
                "Saya tidak bisa membanned admin, Anda tahu aturannya, saya juga."
            )
        mention = (await client.get_users(user_id)).mention
        msg = f"**👤 Dibanned:** {mention}\n**👑 Admin:** {message.from_user.mention}"
        await message.chat.ban_member(user_id)
        await message.reply(msg)
    elif message.command[0] == "mute":
        if message.reply_to_message:
            _id = message.reply_to_message.from_user.id
        else:
            if len(message.command) < 2:
                return await message.reply_text(
                    "Saya tidak dapat menemukan pengguna itu."
                )
            else:
                _id = message.text.split()[1]
        user_id = (await client.get_users(_id)).id
        if user_id == client.me.id:
            return await message.reply_text(
                "Aku tidak bisa membisukan diriku sendiri, aku bisa pergi jika kamu mau."
            )
        if user_id in OWNER_ID:
            return await message.reply_text("Anda Tidak Bisa Membisukan Anggota Ini")
        user = await message.chat.get_member(user_id)
        if user.status == ChatMemberStatus.ADMINISTRATOR:
            return await message.reply_text(
                "Saya tidak bisa membisukan admin, Anda tahu aturannya, saya juga."
            )
        mention = (await client.get_users(user_id)).mention
        msg = f"**👤 Membisukan:** {mention}\n**👑 Admin:** {message.from_user.mention}"
        await message.chat.restrict_member(user_id, ChatPermissions())
        await message.reply(msg)
    elif message.command[0] == "unmute":
        if message.reply_to_message:
            _id = message.reply_to_message.from_user.id
        else:
            if len(message.command) < 2:
                return await message.reply_text(
                    "Saya tidak dapat menemukan pengguna itu."
                )
            else:
                _id = message.text.split()[1]
        user = await client.get_users(_id)
        await message.chat.unban_member(user.id)
        await message.reply(f"**✅ {user.mention} Sudah Bisa Chat Lagi")
    elif message.command[0] == "unban":
        if message.reply_to_message:
            _id = message.reply_to_message.from_user.id
        else:
            if len(message.command) < 2:
                return await message.reply_text(
                    "Saya tidak dapat menemukan pengguna itu."
                )
            else:
                _id = message.text.split()[1]
        user = await client.get_users(_id)
        await message.chat.unban_member(user.id)
        await message.reply(f"**✅ {user.mention} Sudah Join Lagi")


@ubot.on_message(
    filters.group & filters.command(["promote", "fullpromote"], PREFIX) & filters.me
)
async def promotte(client, message):
    user_id = await extract_user(message)
    umention = (await client.get_users(user_id)).mention
    prom = await message.reply("Processing...")
    if not user_id:
        return await prom.edit("Tidak menemukan user tersebut.")
    bot = (
        await client.get_chat_member(message.chat.id, message.from_user.id)
    ).privileges
    if not bot.can_promote_members:
        return await prom.edit("Saya tidak memiliki izin yang cukup")
    if message.command[0] == "fullpromote":
        await client.add_chat_members(message.chat.id, user_id)
        await message.chat.promote_member(
            user_id,
            privileges=ChatPrivileges(
                can_manage_chat=True,
                can_delete_messages=True,
                can_manage_video_chats=True,
                can_restrict_members=True,
                can_change_info=True,
                can_invite_users=True,
                can_pin_messages=True,
                can_promote_members=True,
            ),
        )
        return await prom.edit(f"Fully Promoted! {umention}")
    elif message.command[0] == "promote":
        await client.add_chat_members(message.chat.id, user_id)
        await message.chat.promote_member(
            user_id,
            privileges=ChatPrivileges(
                can_manage_chat=True,
                can_delete_messages=True,
                can_manage_video_chats=True,
                can_restrict_members=True,
                can_change_info=True,
                can_invite_users=True,
                can_pin_messages=True,
                can_promote_members=False,
            ),
        )
        await prom.edit(f"Promoted! {umention}")


@ubot.on_message(filters.group & filters.command("demote", PREFIX) & filters.me)
async def demote(client, message):
    user_id = await extract_user(message)
    prom = await message.reply("Processing...")
    if not user_id:
        return await prom.edit("Tidak menemukan user tersebut.")
    if user_id == message.from_user.id:
        return await prom.edit("Aku tidak bisa demote diriku sendiri.")
    await message.chat.promote_member(
        user_id,
        privileges=ChatPrivileges(
            can_manage_chat=False,
            can_delete_messages=False,
            can_manage_video_chats=False,
            can_restrict_members=False,
            can_change_info=False,
            can_invite_users=False,
            can_pin_messages=False,
            can_promote_members=False,
        ),
    )
    umention = (await client.get_users(user_id)).mention
    await prom.edit(f"Demoted! {umention}")


@ubot.on_message(filters.group & filters.command("settitle", PREFIX) & filters.me)
async def settitles(client, message):
    user_id = await extract_user(message)
    mmk = message.command[1:]
    kontol = " ".join(mmk)
    jem = message.command[2:]
    tai = " ".join(jem)
    title = kontol if message.reply_to_message else tai
    prom = await message.reply("Processing...")
    if not user_id:
        return await prom.edit("Tidak menemukan user tersebut.")
    try:
        await client.set_administrator_title(message.chat.id, user_id, title)
        umention = (await client.get_users(user_id)).mention
        await prom.edit(f"Set title! {umention} - {title}")
    except Exception as e:
        return await prom.edit(f"**INFO :** {e}")


@ubot.on_message(filters.group & filters.command("invite", PREFIX) & filters.me)
async def invite(client, message):
    reply = message.reply_to_message
    yy = await message.reply("Sedang mengundang jamet ke grup...")
    if reply:
        user = reply.from_user["id"]
    else:
        user = get_arg(message)
        if not user:
            await yy.edit("**Anjay ente mau undang siapa?**")
            return
    get_user = await client.get_users(user)
    try:
        await client.add_chat_members(message.chat.id, get_user.id)
        await yy.edit(f"**Menambahkan {get_user.first_name} Kedalam chat!**")
    except Exception as e:
        await yy.edit(f"{e}")


@ubot.on_message(filters.command(["pin", "unpin"], PREFIX) & filters.me)
async def _(c, m):
    chat_id = m.chat.id
    if m.command[0] == "pin":
        if not m.reply_to_message:
            return await m.reply("__Silahkan balas ke pesan__")
        try:
            await c.pin_chat_message(chat_id, m.reply_to_message.id)
            await m.reply(
                f"**Menyematkan pesan [ini]({m.reply_to_message.link})**",
                disable_web_page_preview=True,
            )
        except Exception as e:
            return await m.reply(f"**INFO :** `{e}`")
    elif m.command[0] == "unpin":
        if not m.reply_to_message:
            return await m.reply("__Silahkan balas ke pesan__")
        try:
            await c.unpin_chat_message(chat_id, m.reply_to_message.id)
            await m.reply(
                f"**Melepas sematan pesan [ini]({m.reply_to_message.link})**",
                disable_web_page_preview=True,
            )
        except Exception as e:
            return await m.reply(f"**INFO :** `{e}`")
