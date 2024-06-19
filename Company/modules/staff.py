from pyrogram import filters

from Company import ubot
from Company.config import PREFIX
from Company.modules.bot import add_command_help

add_command_help(
    "staff",
    [
        ["staff", "Untuk mengetahui daftar semua admin didalam grup."],
    ],
)


@ubot.on_message(filters.me & filters.command("staff", PREFIX) & filters.group)
async def staff_func_(_, m):
    chat_title = m.chat.title
    creator = []
    co_founder = []
    admin = []
    async for x in m.chat.get_members():
        mention = (
            f"{x.user.first_name} {x.user.last_name or ''}"
            if x.user.username is None
            else f"@{x.user.username}"
        )
        if (
            x.status.value == "administrator"
            and x.privileges
            and x.privileges.can_promote_members
        ):
            if x.custom_title:
                co_founder.append(f"├ {mention} - {x.custom_title}")
            else:
                co_founder.append(f"├ {mention}")
        elif x.status.value == "administrator":
            if x.custom_title:
                admin.append(f"├ {mention} - {x.custom_title}")
            else:
                admin.append(f"├ {mention}")
        elif x.status.value == "owner":
            if x.custom_title:
                creator.append(f"└ {mention} - {x.custom_title}")
            else:
                creator.append(f"└ {mention}")
    if not co_founder and not admin:
        result = f"""
**STAFF GRUP
{chat_title}

👑 Owner:
{creator[0]}**"""
    elif not co_founder:
        adm = admin[-1].replace("├", "└")
        admin.pop(-1)
        admin.append(adm)
        result = f"""
**STAFF GRUP
{chat_title}

👑 Owner:
{creator[0]}

👮 Admin:**
""" + "\n".join(
            admin
        )
    elif not admin:
        cof = co_founder[-1].replace("├", "└")
        co_founder.pop(-1)
        co_founder.append(cof)
        result = f"""
**STAFF GRUP
{chat_title}

👑 Owner:
{creator[0]}

👮 Co-Founder:**
""" + "\n".join(
            co_founder
        )
    else:
        adm = admin[-1].replace("├", "└")
        admin.pop(-1)
        admin.append(adm)
        cof = co_founder[-1].replace("├", "└")
        co_founder.pop(-1)
        co_founder.append(cof)
        result = (
            (
                f"""
**STAFF GRUP
{chat_title}

👑 Owner:
{creator[0]}

👮 Co-Founder:**
"""
                + "\n".join(co_founder)
                + """

**👮 Admin:**
"""
            )
            + "\n".join(admin)
        )

    await m.reply(result)
