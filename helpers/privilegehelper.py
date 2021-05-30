from aiohttp_session import get_session
from common.helpers import userhelper # type: ignore

async def logged_in(r):
    session = await get_session(r)
    if session.get("user_id"): return True
    return False

async def is_admin(r):
    session = await get_session(r)
    user = await userhelper.get_user(session["user_id"])
    if "7" in str(user.privileges): return True
    return False