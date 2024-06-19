import os
import asyncio

from pyrogram.types import Message

from Company import ubot
from Company.config import PREFIX
from Company.modules.bot import add_command_help
from Company.utils.data import *



add_command_help(
    "zombies",
    [
        ["zombies", "`.zombies`, Untuk mengeluarkan akun depresi dalam grup."],
    ],
)


@ubot.on_message(filters.command("zombies", PREFIX) & filters.me)
async def zombies_handler(c, m: Message):
    deac_user = m.command[1] if len(m.command) > 1 else m.reply_to_message.from_user.id if m.reply_to_message and m.reply_to_message.from_user else None
    temp_count = 0
    admin_count = 0
    count = 0
    
    if deac_user:
        return await m.send_edit("Checking deleted accounts . . ."
        )
    try:
        count = await c.get_users(deac_user)
    except:
        return await m.reply("__Tidak menemukan user tersebut__")

        async for x in c.get_chat_members(chat_id=m.chat.id):
            if x.user.is_deleted:
                temp_count += 1

        if temp_count > 0:
            await m.send_edit(f"**Found:** `{temp_count}` Deleted accounts\nUse `{c.Trigger[0]}zombies clean` to remove them from group.")
        else:
            await m.send_edit("No deleted accounts found.\nGroup is clean as Hell ! 😃", delme=3)

    
        await m.send_edit("Cleaning deleted accounts . . .")

        async for x in c.get_chat_members(chat_id=m.chat.id):
            if x.user.is_deleted:
                if x.status in ("administrator", "creator"):
                    admin_count += 1
                    continue
                try:
                    await c.ban_chat_member(
                        chat_id=m.chat.id,
                        user_id=x.user.id
                    )
                    count += 1
                    await asyncio.sleep(0.2)
                except Exception as e:
                    await c.error(e)
        await m.send_edit(f"`Group clean up done !`\n\n**Total:** `{count+admin_count}`\n**Removed:** `{count}`\n**Not Removed:** `{admin_count}`\n\n**Note:** `Not removed accounts can be admins or the owner`")


        await m.send_edit(f"Check `{c.Trigger[0]}help zombies` to see how it works !")
    else:
        await m.send_edit("Something went wrong, please try again later !", delme=3)
