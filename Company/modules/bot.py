from datetime import datetime
from time import time
from pyrogram.types import *
from platform import python_version

import psutil
from pyrogram import __version__, filters
from Company import CMD_HELP, bot, ubot
from Company.config import *
from Company.utils.data import *
from Company.utils.inline import paginate_help
from Company.utils.misc import *

START_TIME = datetime.utcnow()
TIME_DURATION_UNITS = (
    ("Minggu", 60 * 60 * 24 * 7),
    ("Hari", 60 * 60 * 24),
    ("Jam", 60 * 60),
    ("Menit", 60),
    ("Detik", 1),
)


async def _human_time_duration(seconds):
    if seconds == 0:
        return "inf"
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append(f'{amount} {unit}{"" if amount == 1 else ""}')
    return ", ".join(parts)


msg = "**Help Menu Open :**\n{}\n{}"

@ubot.on_message(filters.user(OWNER_ID) & filters.command("Onecuk", PREFIX))
async def _(c, m):
    await m.reply("Mwaaah 🥵")
    
    
@bot.on_inline_query(filters.regex("help"))
async def _(client, inline_query):
    bttn = paginate_help(0, CMD_HELP, "helpme")
    ex = await logo_info(inline_query.from_user.id)
    logo = "https://telegra.ph/file/5b913c3dd3f72b5d8ae35.jpg" if ex is None else ex
    pr = "**Prefix:**"
    for i in PREFIX:
        pr += f" `{i}`"
    mod = f"**Modules:** `{len(CMD_HELP)}` Modul"
    await client.answer_inline_query(
        inline_query.id,
        cache_time=0,
        results=[
            (
                InlineQueryResultPhoto(
                    photo_url=logo,
                    thumb_url=logo,
                    title="Help Menu!",
                    caption=msg.format(mod, pr),
                    reply_markup=InlineKeyboardMarkup(bttn),
                )
            )
        ],
    )


@bot.on_callback_query(filters.regex("helpme_prev\((.+?)\)"))
async def on_plug_prev_in_cb(_, callback_query: CallbackQuery):
    pr = "**Prefix:**"
    for i in PREFIX:
        pr += f" `{i}`"
    mod = f"**Modules:** `{len(CMD_HELP)}` Modul"
    current_page_number = int(callback_query.matches[0].group(1))
    buttons = paginate_help(current_page_number - 1, CMD_HELP, "helpme")
    await callback_query.edit_message_text(
        msg.format(mod, pr),
        reply_markup=InlineKeyboardMarkup(buttons),
    )


@bot.on_callback_query(filters.regex("helpme_next\((.+?)\)"))
async def on_plug_next_in_cb(_, callback_query: CallbackQuery):
    pr = "**Prefix:**"
    for i in PREFIX:
        pr += f" `{i}`"
    mod = f"**Modules:** `{len(CMD_HELP)}` Modul"
    current_page_number = int(callback_query.matches[0].group(1))
    buttons = paginate_help(current_page_number + 1, CMD_HELP, "helpme")
    await callback_query.edit_message_text(
        msg.format(mod, pr),
        reply_markup=InlineKeyboardMarkup(buttons),
    )


@bot.on_callback_query(filters.regex("ub_modul_(.*)"))
async def on_plug_in_cb(_, callback_query: CallbackQuery):
    modul_name = callback_query.matches[0].group(1)
    commands: dict = CMD_HELP[modul_name]
    this_command = (
        f"──「 **Help For {str(modul_name[0].upper() + modul_name[1:])}** 」──\n\n"
    )
    for x in commands:
        this_command += (
            f"  •  **Command:** `?{str(x)}`\n  •  **Function:** {str(commands[x])}\n\n"
        )
    this_command += "© @FredXUbot"
    bttn = [
        [InlineKeyboardButton(text="• Kembali •", callback_data="reopen")],
    ]
    await callback_query.edit_message_text(
        this_command,
        reply_markup=InlineKeyboardMarkup(bttn),
    )


@bot.on_callback_query(filters.regex("reopen"))
async def reopen_in_cb(_, callback_query: CallbackQuery):
    pr = "**Prefix:**"
    for i in PREFIX:
        pr += f" `{i}`"
    mod = f"**Modules:** `{len(CMD_HELP)}` Modul"
    buttons = paginate_help(0, CMD_HELP, "helpme")
    await callback_query.edit_message_text(
        msg.format(mod, pr),
        reply_markup=InlineKeyboardMarkup(buttons),
    )


@ubot.on_message(filters.command("help", PREFIX) & filters.me)
async def help(client, message):
    help_arg = get_arg(message)
    if not help_arg:
        nice = await client.get_inline_bot_results(bot.me.username, message.command[0])
        await message.reply_inline_bot_result(nice.query_id, nice.results[0].id)

    if help_arg:
        if help_arg in CMD_HELP:
            commands: dict = CMD_HELP[help_arg]
            this_command = (
                f"──「 **Help For {str(help_arg[0].upper() + help_arg[1:])}** 」──\n\n"
            )
            for x in commands:
                this_command += f"  •  **Command:** `?{str(x)}`\n  •  **Function:** `{str(commands[x])}`\n\n"
            this_command += "© @FredXUbot"
            await message.reply(this_command, parse_mode=enums.ParseMode.MARKDOWN)
        else:
            await message.reply(
                f"`{help_arg}` **Bukan Nama Modul yang Valid.**",
                parse_mode=enums.ParseMode.MARKDOWN,
            )


def add_command_help(module_name, commands):
    if module_name in CMD_HELP.keys():
        command_dict = CMD_HELP[module_name]
    else:
        command_dict = {}

    for x in commands:
        for y in x:
            if y is not x:
                command_dict[x[0]] = x[1]

    CMD_HELP[module_name] = command_dict


@bot.on_inline_query(filters.regex("about"))
async def _(client, inline_query):
    user = inline_query.from_user.id
    dc_id = inline_query.from_user.dc_id
    start = time()
    xd = await all_pm(user)
    bd = await all_grup(user)
    pm = "0" if xd is False else len(xd)
    grup = "0" if bd is False else len(bd)
    current = datetime.utcnow()
    uptime_sec = (current - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    delta_ping = time() - start
    if user in OWNER_ID:
        status = "Owner"
    else:
        status = "Member"
    msg = f"""
**FredXUbott**
    **status:** **__FredXUbot [{status}]__**
        **dc:** `{dc_id}`
        **ping_dc:** `{delta_ping * 1000:.3f} ms`
        **userbot:** `{len(ubot._ubot)} user`
        **peer_user:** `{pm}`
        **peer_group:** `{grup}`
        **Company_uptime:** `{uptime}`
"""
    await client.answer_inline_query(
        inline_query.id,
        cache_time=0,
        results=[
            (
                InlineQueryResultArticle(
                    thumb_url="https://telegra.ph/file/5b913c3dd3f72b5d8ae35.jpg",
                    title="About",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    "⟨ Support ⟩", url="t.me/FredXUbot"
                                ),
                            ],
                        ]
                    ),
                    input_message_content=InputTextMessageContent(msg),
                )
            )
        ],
    )


@ubot.on_message(filters.me & filters.command("ping", PREFIX))
async def ping_(c, m):
    x = await m.reply("Ping....")
    ping = round((datetime.now() - m.date).microseconds / int(1e6), 2)
    current = datetime.utcnow()
    uptime_sec = (current - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    xping = f"""
**PING:** **{ping}** ms
**TIMER:** **{uptime}**
"""
    await x.edit(xping)


@ubot.on_message(filters.me & filters.command(["about", "bot"], PREFIX))
async def _(client, message):
    text = message.command[0]
    x = await client.get_inline_bot_results(bot.me.username, text)
    await message.reply_inline_bot_result(x.query_id, x.results[0].id)


@bot.on_inline_query(filters.regex("bot"))
async def _(client, inline_query):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    cpu = psutil.cpu_percent(interval=0.5)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    msg = f"""
**USERBOT:** {bot.me.mention}

**CPU:** `{cpu}%`
**RAM:** `{mem}%`
**DISK:** `{disk}%`

**Platfrom Version**
Python: `{python_version()}`
Pyrogram: `{__version__}`

**Total Modules:** 
`{len(CMD_HELP)}` Modules 

**Total Userbot:** 
`{len(ubot._ubot)}` Userbot 

**Activated**
`{uptime}`
"""
    await client.answer_inline_query(
        inline_query.id,
        cache_time=0,
        results=[
            (
                InlineQueryResultArticle(
                    thumb_url="https://telegra.ph/file/5b913c3dd3f72b5d8ae35.jpg",
                    title="Platform Version",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    "• Refresh •", callback_data="refresh"
                                )
                            ],
                        ]
                    ),
                    input_message_content=InputTextMessageContent(msg),
                )
            )
        ],
    )


@bot.on_callback_query(filters.regex("refresh"))
async def _(client, callback_query):
    await callback_query.answer("✅ Refresh Successfully Executed", True)
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    cpu = psutil.cpu_percent(interval=0.5)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    msg = f"""
**USERBOT:** {bot.me.mention}

**CPU:** `{cpu}%`
**RAM:** `{mem}%`
**DISK:** `{disk}%`

**Platfrom Version**
Python: `{python_version()}`
Pyrogram: `{__version__}`

**Total Modules:** 
`{len(CMD_HELP)}` Modules 

**Total Userbot:** 
`{len(ubot._ubot)}` Userbot 

**Activated**
`{uptime}`
"""
    await callback_query.edit_message_text(
        msg,
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("• Refresh •", callback_data="refresh")],
            ]
        ),
    )

