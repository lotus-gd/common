from common.globals import sql

async def get_top_100():
    users = await sql.fetchall("SELECT name, pp FROM users ORDER BY pp DESC LIMIT 100")
    return users

async def get_top_100_stars():
    users = await sql.fetchall("SELECT name, stars FROM users ORDER BY stars DESC LIMIT 100")
    return users