import asyncio

from motor.motor_asyncio import AsyncIOMotorClient

from pyrogram import filters
from Company.config import MONGO_URL


mongo_client = AsyncIOMotorClient(MONGO_URL)
mongodb = mongo_client.Company

ubotdb = mongodb.ubot
grupdb = mongodb.grup
pmdb = mongodb.pm
blcdb = mongodb.blchat
gbandb = mongodb.gban
configdb = mongodb.config
notedb = mongodb.notes
sudodb = mongodb.sudoers



# ubot
async def add_ubot(user_id, api_id, api_hash, session_string):
    user = await ubotdb.find_one({"user_id": user_id})
    if user:
        await ubotdb.update_one(
            {"user_id": user_id},
            {
                "$set": {
                    "api_id": api_id,
                    "api_hash": api_hash,
                    "session_string": session_string,
                }
            },
        )
    else:
        await ubotdb.insert_one(
            {
                "user_id": user_id,
                "api_id": api_id,
                "api_hash": api_hash,
                "session_string": session_string,
            }
        )


async def remove_ubot(user_id):
    return await ubotdb.delete_one({"user_id": user_id})


async def get_userbots():
    data = []
    async for ubot in ubotdb.find({"user_id": {"$exists": 1}}):
        data.append(
            dict(
                name=str(ubot["user_id"]),
                api_id=ubot["api_id"],
                api_hash=ubot["api_hash"],
                session_string=ubot["session_string"],
            )
        )
    return data


# grup input
async def add_grup(user_id, grup):
    cek = await grupdb.find_one({"user_id": user_id, "grup": grup})
    if cek:
        await grupdb.update_one(
            {"user_id": user_id},
            {
                "$set": {
                    "grup": grup,
                }
            },
        )
    else:
        await grupdb.insert_one({"user_id": user_id, "grup": grup})


async def grup_info(user_id, grup):
    r = await grupdb.find_one({"user_id": user_id, "grup": grup})
    if r:
        return r
    else:
        return False


async def all_grup(user_id):
    r = [jo async for jo in grupdb.find({"user_id": user_id})]
    if r:
        return r
    else:
        return False


# user input
async def add_pm(user_id, user):
    cek = await pmdb.find_one({"user_id": user_id, "user": user})
    if cek:
        await pmdb.update_one(
            {"user_id": user_id},
            {
                "$set": {
                    "user": user,
                }
            },
        )
    else:
        await pmdb.insert_one({"user_id": user_id, "user": user})


async def pm_info(user_id, user):
    r = await pmdb.find_one({"user_id": user_id, "user": user})
    if r:
        return r
    else:
        return False


async def all_pm(user_id):
    r = [jo async for jo in pmdb.find({"user_id": user_id})]
    if r:
        return r
    else:
        return False


# blacklist chat
async def add_black(user_id, grup, title):
    cek = await blcdb.find_one({"user_id": user_id, "grup": grup})
    if cek:
        await grupdb.update_one(
            {"user_id": user_id},
            {"$set": {"grup": grup, "title": title}},
        )
    else:
        await blcdb.insert_one({"user_id": user_id, "grup": grup, "title": title})


async def del_black(user_id, grup):
    await blcdb.delete_one({"user_id": user_id, "grup": grup})


async def black_info(user_id, grup):
    r = await blcdb.find_one({"user_id": user_id, "grup": grup})
    if r:
        return r
    else:
        return False


async def all_black(user_id):
    r = [jo async for jo in blcdb.find({"user_id": user_id})]
    if r:
        return r
    else:
        return []


# gban input
async def add_gban(user_id, user, nama):
    cek = await gbandb.find_one({"user_id": user_id, "user": user})
    if cek:
        await pmdb.update_one(
            {"user_id": user_id},
            {
                "$set": {
                    "user": user,
                    "nama": nama,
                }
            },
        )
    else:
        await gbandb.insert_one({"user_id": user_id, "user": user, "nama": nama})


async def del_gban(user_id, user):
    await gbandb.delete_one({"user_id": user_id, "user": user})


async def all_gban(user_id):
    r = [jo async for jo in gbandb.find({"user_id": user_id})]
    if r:
        return r
    else:
        return False


# config
async def add_config(user_id, logo, log, pmlog, gruplog):
    user = await configdb.find_one({"_id": user_id})
    if user:
        await configdb.update_one(
            {"_id": user_id},
            {
                "$set": {
                    "logo": logo,
                    "log": log,
                    "pmlog": pmlog,
                    "gruplog": gruplog,
                }
            },
        )
    else:
        await configdb.insert_one(
            {
                "_id": user_id,
                "logo": logo,
                "log": log,
                "pmlog": pmlog,
                "gruplog": gruplog,
            }
        )


async def cek_config(user_id):
    r = [jo async for jo in configdb.find({"_id": user_id})]
    if r:
        return r
    else:
        return False


async def logo_info(user_id):
    r = await configdb.find_one({"_id": user_id})
    if not r:
        return None
    return r["logo"]


async def log_info(user_id):
    r = await configdb.find_one({"_id": user_id})
    if not r:
        return None
    return r["log"]


async def pmlog_info(user_id):
    r = await configdb.find_one({"_id": user_id})
    if not r:
        return "on"
    return r["pmlog"]


async def gruplog_info(user_id):
    r = await configdb.find_one({"_id": user_id})
    if not r:
        return "on"
    return r["gruplog"]


# notes
async def add_note(note_name, user_id, note_id):
    result = await notedb.find_one({"note_name": note_name, "user_id": user_id})
    if result:
        await notedb.update_one(
            {"note_name": note_name},
            {"$set": {"user_id": user_id, "note_id": note_id}},
        )
    else:
        await notedb.insert_one(
            {"note_name": note_name, "user_id": user_id, "note_id": note_id}
        )


async def del_note(note_name, user_id):
    await notedb.delete_one({"note_name": note_name, "user_id": user_id})


async def note_info(note_name, user_id):
    r = await notedb.find_one({"note_name": note_name, "user_id": user_id})
    if r:
        return r
    else:
        return False


async def all_note(user_id):
    r = [u async for u in notedb.find({"user_id": user_id})]
    if r:
        return r
    else:
        return False

#sudoers
async def get_sudo():
    sudo_users = await sudodb.find_one({"sudo": "sudo"})
    if not sudo_users:
        return []
    return sudo_users["sudoers"]


async def add_sudo(user_id):
    sudo_users = await get_sudo()
    sudo_users.append(user_id)
    await sudodb.update_one(
        {"sudo": "sudo"},
        {
            "$set": {
                "sudoers": sudo_users
            }
        },
        upsert=True
    )
    return True


async def remove_sudo(user_id):
    sudo_users = await get_sudo()
    sudo_users.remove(user_id)
    await sudodb.update_one(
        {"sudo": "sudo"},
        {
            "$set": {
                "sudoers": sudo_users
            }
        },
        upsert=True
    )
    return True



