# Idk what to do so i will just make a botch attempt to solve this.
from common.helpers.cache import Cache
from common.db.mysql import MySQLPool
from common.config import config
import os

# Windows compatibillity.
if os.name == "nt":
    import asyncio
    loop = asyncio.get_event_loop()
else:
    import uvloop
    loop = uvloop.new_event_loop()

sql = MySQLPool()

user_cache = Cache(
    20,
    200
)

# These are dicts as we NEVER want to drop them.
privilege_cache: dict = {}
badge_cache: dict = {}


async def connect_sql():
    global sql
    connected = True
    sql = await MySQLPool.connect(
        config["db_host"],
        config["db_user"],
        config["db_password"],
        config["db_database"],
        config["db_port"],
        loop
    )

async def pre_cache_privs() -> None:
    """Pre-loads all of the privilege groups."""
    ...

# List of coros that have to be ran on startup.
STARTUP_COROS = (
    connect_sql,
    pre_cache_privs
)

async def startup_init() -> None:
    """Performs a series of tasks required for startup."""

    for coro in STARTUP_COROS:
        await coro()
