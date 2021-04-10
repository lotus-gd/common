from common.globals import sql

async def get_top_100():
    users = await sql.fetchall("SELECT username, pp FROM accounts ORDER BY pp DESC;")
    return users
