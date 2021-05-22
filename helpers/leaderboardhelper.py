from common.globals import sql

async def get_top_100():
    users = await sql.fetchall("SELECT name, pp FROM users ORDER BY pp DESC LIMIT 100")
    return users
