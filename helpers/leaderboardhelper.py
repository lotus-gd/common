from common.globals import connect_sql, sql, connected
from common.config import config

async def get_top_100():
    if not connected:
        await connect_sql()
    users = await sql.fetchall("SELECT username, pp FROM accounts ORDER BY pp DESC;")
    return users
