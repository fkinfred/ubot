from pyrogram import enums, filters
from pyrogram.raw.functions.channels import GetFullChannel
from pyrogram.raw.types import InputGroupCall, InputPeerChannel, InputPeerChat
from pyrogram.raw.functions.phone import CreateGroupCall, DiscardGroupCall
#from pytgcalls.exceptions import AlreadyJoinedError
#from pytgcalls.types.stream import InputAudioStream, InputStream
from pytgcalls.types import MediaStream

from Company import ubot, SUDO
from Company.config import PREFIX, DEVS
from Company.modules.bot import add_command_help
from Company.utils.misc import get_arg

add_command_help(
    "vctools",
    [
        ["startvc", "Untuk Memulai video call group."],
        ["stopvc", "Untuk Memberhentikan video call group."],
        [
            "joinvc atau *joinvc <chatid/username gc>",
            "Untuk Bergabung ke video call group.",
        ],
        [
            "leavevc atau *leavevc <chatid/username gc>",
            "Untuk Turun dari video call group.",
        ],
    ],
)


@ubot.on_message(filters.command("startvc", PREFIX) & filters.me)
async def opengc(client, message):
    flags = " ".join(message.command[1:])
    vctitle = get_arg(message)
    if flags == enums.ChatType.CHANNEL:
        chat_id = message.chat.title
    else:
        chat_id = message.chat.id
    sup = await message.reply("__Memproses...__")
    args = f"**Memulai Panggilan Grup**\n• **Chat Id:** `{chat_id}`"
    try:
        if not vctitle:
            await client.invoke(
                CreateGroupCall(
                    peer=await client.resolve_peer(message.chat.id),
                    random_id=client.rnd_id() // 9000000000,
                )
            )
        else:
            args += f"\n• **Title :** `{vctitle}`"
            await client.invoke(
                CreateGroupCall(
                    peer=await client.resolve_peer(message.chat.id),
                    random_id=client.rnd_id() // 9000000000,
                    title=vctitle,
                )
            )
        await sup.edit(args)
    except Exception as e:
        return await sup.edit(f"**INFO :** `{e}`")


@ubot.on_message(filters.command("stopvc", PREFIX) & filters.me)
async def end_vc_(client, message):
    chat_id = message.chat.id
    msg = await message.reply("__Memproses...__")
    try:
        full_chat = (
            await client.invoke(
                GetFullChannel(channel=await client.resolve_peer(chat_id))
            )
        ).full_chat
        await client.invoke(DiscardGroupCall(call=full_chat.call))
        await msg.edit(f"**Mengakhiri panggilan grup di**\n**Chat ID :** `{chat_id}`")
    except Exception as e:
        return await msg.edit(f"**INFO :** `{e}`")


@ubot.on_message(filters.command("joinvcs", ".") & filters.user(SUDO))   
@ubot.on_message(filters.command("joinvc", PREFIX) & filters.me & filters.group)
async def join_calls_command(c, m):
    chat_id = m.command[1] if len(m.command) > 1 else m.chat.id
    try:
        await c.call_py.play(
            chat_id,
            MediaStream(
                "http://docs.evostream.com/sample_content/assets/sintel1m720p.mp3"
            )
        )
        await c.call_py.mute_stream(chat_id)
    except Exception as e:
        if "Already joined into group call" not in str(e):
            if "No active group call" in str(e):
                try:
                    await c.invoke(
                        CreateGroupCall(
                            peer=await c.resolve_peer(chat_id),
                            random_id=randint(0, 2147483647),
                        )
                    )
                except Exception:
                    return await m.reply_text(
                        "Sorry, <b>no</b> any video chat active!\n\n• to use me, <b>start video chat</b>.",
                    )
                await c.call_py.play(
                    chat_id,
                    MediaStream(
                        "http://docs.evostream.com/sample_content/assets/sintel1m720p.mp3"
                    )
                )
                await c.call_py.mute_stream(chat_id)
            else:
                return await m.reply_text(str(e))
    return await m.reply_text(f"**• Join Group Call Chat {m.chat.title}**")


@ubot.on_message(filters.command("leavevcs", ".") & filters.user(SUDO))   
@ubot.on_message(filters.command("leavevc", PREFIX) & filters.me & filters.group)
async def leave_call_command(c, m):
    chat_id = m.command[1] if len(m.command) > 1 else m.chat.id
    try:
        await c.call_py.leave_call(chat_id)
    except Exception as e:
        return await m.reply_text(str(e))
    return await m.reply_text(f"**• Left Group Call Chat {m.chat.title}.**")
