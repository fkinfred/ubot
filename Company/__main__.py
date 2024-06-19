import importlib
from sys import version as pyver
import asyncio
from atexit import register

from pyrogram import __version__ as pyrover
from pyrogram import idle
from pyrogram.errors import RPCError

from Company import Ubot, bot, ubot, LOOP, loadSuoder
from Company.modules import ALL_MODULES
from Company.utils.data import get_userbots, log_info, remove_ubot

from .config import *

msg = """
🔥 **FredXUbot Berhasil Di Aktifkan**
━━
➠ **Python Version** > `{}`
➠ **Pyrogram Version** > `{}`
━━
"""


async def auto_restart():
    while not await asyncio.sleep(3000):
        def _():
            os.system(f"kill -9 {os.getpid()} && python3 -m Company")
        register(_)
        sys.exit(0)


async def main():
    await loadSuoder()
    await bot.start()
    await ubot.start()
    print(f"{ubot.me.first_name} Telah aktif")
    for _ubot in await get_userbots():
        ubot_ = Ubot(**_ubot)
        try:
            await ubot_.start()
            print(f"{ubot_.me.first_name} Telah aktif")
            anu = await log_info(ubot_.me.id)
            log = "me" if anu is None else anu
            await ubot_.send_message(log, msg.format(pyver.split()[0], pyrover))
        except RPCError as e:
            await remove_ubot(int(_ubot["name"]))
            print(f"✅ {_ubot['name']} Berhasil Dihapus Dari Database")
   
    for all_module in ALL_MODULES:
        importlib.import_module(f"Company.modules.{all_module}")
    print(f"[🤖 @{bot.me.username} 🤖] [🔥 BERHASIL DIAKTIFKAN! 🔥]")
    await bot.send_message(LOG_GRP, msg.format(pyver.split()[0], pyrover))
    await auto_restart()
    await idle()


if __name__ == "__main__":
    LOOP.run_until_complete(main())
