# companyubot

import sys
from typing import Callable
import asyncio
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.handlers import MessageHandler
from pyromod import listen
from pytgcalls import PyTgCalls

from .utils.data import *
from .config import *

LOOP = asyncio.get_event_loop()
SUDO_USERS.append("OWNER_ID")
SUDO = []
CMD_HELP = {}



if not API_ID:
    print("API_ID Tidak ada")
    sys.exit()

if not API_HASH:
    print("API_HASH Tidak ada")
    sys.exit()

if not BOT_TOKEN:
    print("BOT_TOKEN Tidak ada")
    sys.exit()

if not LOG_GRP:
    print("LOG_GRP Tidak ada")
    sys.exit()

if not MONGO_URL:
    print("MONGO_URL Tidak ada")
    sys.exit()

if not SESSION_STRING:
    print("SESSION_STRING Tidak ada")
    sys.exit()


bot = Client(
    name="CompanyUbot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)


class Ubot(Client):
    __module__ = "pyrogram.client"
    _ubot = []
    _dialogue: object = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.call_py = PyTgCalls(self)
        
    def on_message(self, filters=None, group=0):
        def decorator(func):
            for ub in self._ubot:
                ub.add_handler(MessageHandler(func, filters), group)
            return func

        return decorator

    async def start(self):
        from .utils.data import all_black, get_sudo

        await super().start()
        await self.call_py.start()
        if self not in self._ubot:
            self._ubot.append(self)
        arrayBlGcast = await all_black(self.me.id)
        arrayNull = []
        for x in arrayBlGcast:
            arrayNull.append(int(x['grup']))
        self._dialogue[self.me.id] = arrayNull


ubot = Ubot(
    name="CompanyUbot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING,
)


async def loadSuoder():
    from .utils.data import get_sudo
    
    sudoer = await get_sudo()
    for x in sudoer:
        if x not in SUDO:
            SUDO.append(x)
    for z in DEVS:
        if z not in SUDO:
            SUDO.append(z)
    print(f'SUDOERS LOADED WITH {SUDO} USER')
