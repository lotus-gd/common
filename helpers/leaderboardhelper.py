from common.db.mysql import get_db
from common.config import config

async def get_top_100():
    db = await get_db()
    users = await db.fetchall("SELECT username, pp FROM accounts ORDER BY pp DESC;")
    return users
