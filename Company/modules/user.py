from asyncio import gather
from os import remove

from pyrogram import filters
from pyrogram.enums import ChatType

from Company import ubot
from Company.config import PREFIX
from Company.modules.bot import add_command_help
from Company.utils.misc import extract_user

add_command_help(
    "info",
    [
        [
            "info <username/userid/reply>",
            "dapatkan info pengguna telegram dengan deskripsi lengkap.",
        ],
        [
            "cinfo <username/chatid/reply>",
            "dapatkan info group dengan deskripsi lengkap.",
        ],
        ["id", "Cek id user atau group atau channel"],
        ["ping", "Cek kecepatan ubot"],
        ["about", "alive ubot"],
    ],
)


@ubot.on_message(filters.me & filters.command(["whois", "info"], PREFIX))
async def _(client, message):
    user_id = await extract_user(message)
    Tm = await message.reply("**Processing . . .**")
    if not user_id:
        return await Tm.edit(
            "**Berikan userid/username/reply untuk mendapatkan info pengguna tersebut.**"
        )
    try:
        user = await client.get_users(user_id)
        username = f"@{user.username}" if user.username else "-"
        first_name = f"{user.first_name}" if user.first_name else "-"
        last_name = f"{user.last_name}" if user.last_name else "-"
        fullname = (
            f"{user.first_name} {user.last_name}" if user.last_name else user.first_name
        )
        user_details = (await client.get_chat(user.id)).bio
        bio = f"{user_details}" if user_details else "-"
        h = f"{user.status}"
        if h.startswith("UserStatus"):
            y = h.replace("UserStatus.", "")
            status = y.capitalize()
        else:
            status = "-"
        dc_id = f"{user.dc_id}" if user.dc_id else "-"
        common = await client.get_common_chats(user.id)
        out_str = f"""**USER INFORMATION:**

🆔 **User ID:** `{user.id}`
👤 **First Name:** {first_name}
🗣️ **Last Name:** {last_name}
🌐 **Username:** {username}
🏛️ **DC ID:** `{dc_id}`
🤖 **Is Bot:** `{user.is_bot}`
🚷 **Is Scam:** `{user.is_scam}`
🚫 **Restricted:** `{user.is_restricted}`
✅ **Verified:** `{user.is_verified}`
⭐ **Premium:** `{user.is_premium}`
📝 **User Bio:** {bio}

👀 **Same groups seen:** {len(common)}
👁️ **Last Seen:** `{status}`
🔗 **User permanent link:** [{fullname}](tg://user?id={user.id})
"""
        photo_id = user.photo.big_file_id if user.photo else None
        if photo_id:
            photo = await client.download_media(photo_id)
            await gather(
                Tm.delete(),
                client.send_photo(
                    message.chat.id,
                    photo,
                    caption=out_str,
                    reply_to_message_id=message.id,
                ),
            )
            remove(photo)
        else:
            await Tm.edit(out_str, disable_web_page_preview=True)
    except Exception as e:
        return await Tm.edit(f"INFO: `{e}`")


@ubot.on_message(filters.me & filters.command(["cwhois", "cinfo"], PREFIX))
async def _(client, message):
    Tm = await message.reply("**Processing . . .**")
    try:
        if len(message.command) > 1:
            chat_u = message.command[1]
            chat = await client.get_chat(chat_u)
        else:
            if message.chat.type == ChatType.PRIVATE:
                return await Tm.edit(
                    f"Gunakan perintah ini di dalam grup atau gunakan !cinfo [group username atau id]"
                )
            else:
                chatid = message.chat.id
                chat = await client.get_chat(chatid)
        h = f"{chat.type}"
        if h.startswith("ChatType"):
            y = h.replace("ChatType.", "")
            type = y.capitalize()
        else:
            type = "Private"
        username = f"@{chat.username}" if chat.username else "-"
        description = f"{chat.description}" if chat.description else "-"
        dc_id = f"{chat.dc_id}" if chat.dc_id else "-"
        out_str = f"""**CHAT INFORMATION:**

🆔 **Chat ID:** `{chat.id}`
👥 **Title:** {chat.title}
👥 **Username:** {username}
📩 **Type:** `{type}`
🏛️ **DC ID:** `{dc_id}`
🗣️ **Is Scam:** `{chat.is_scam}`
🎭 **Is Fake:** `{chat.is_fake}`
✅ **Verified:** `{chat.is_verified}`
🚫 **Restricted:** `{chat.is_restricted}`
🔰 **Protected:** `{chat.has_protected_content}`

🚻 **Total members:** `{chat.members_count}`
📝 **Description:**
`{description}`
"""
        photo_id = chat.photo.big_file_id if chat.photo else None
        if photo_id:
            photo = await client.download_media(photo_id)
            await gather(
                Tm.delete(),
                client.send_photo(
                    message.chat.id,
                    photo,
                    caption=out_str,
                    reply_to_message_id=message.id,
                ),
            )
            remove(photo)
        else:
            await Tm.edit(out_str, disable_web_page_preview=True)
    except Exception as e:
        return await Tm.edit(f"INFO: `{e}`")


@ubot.on_message(filters.me & filters.command("id", PREFIX))
async def cek_id(c, m):
    rep = m.reply_to_message
    if not rep:
        await m.reply(f"**User ID:** `{m.from_user.id}`\n**Chat ID:** `{m.chat.id}`")
        return
    if rep.text:
        await m.reply(f"**User ID:** `{rep.from_user.id}`\n**Chat ID:** `{m.chat.id}`")
        return
    if rep.video:
        await m.reply(
            f"**User ID:** `{rep.from_user.id}`\n**Chat ID:** `{m.chat.id}`\n**File ID:** `{rep.video.file_id}`"
        )
        return
    if rep.photo:
        await m.reply(
            f"**User ID:** `{rep.from_user.id}`\n**Chat ID:** `{m.chat.id}`\n**File ID:** `{rep.photo.file_id}`"
        )
        return
    if rep.voice:
        await m.reply(
            f"**User ID:** `{rep.from_user.id}`\n**Chat ID:** `{m.chat.id}`\n**File ID:** `{rep.voice.file_id}`"
        )
        return
    if rep.audio:
        await m.reply(
            f"**User ID:** `{rep.from_user.id}`\n**Chat ID:** `{m.chat.id}`\n**File ID:** `{rep.audio.file_id}`"
        )
        return
    if rep.sticker:
        await m.reply(
            f"**User ID:** `{rep.from_user.id}`\n**Chat ID:** `{m.chat.id}`\n**File ID:** `{rep.sticker.file_id}`"
        )
        return
    if rep.animation:
        await m.reply(
            f"**User ID:** `{rep.from_user.id}`\n**Chat ID:** `{m.chat.id}`\n**File ID:** `{rep.animation.file_id}`"
        )
        return
    if rep.document:
        await m.reply(
            f"**User ID:** `{rep.from_user.id}`\n**Chat ID:** `{m.chat.id}`\n**File ID:** `{rep.document.file_id}`"
        )
        return
