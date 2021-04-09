from db.mysql import get_db
from config import config

async def get_top_100():
    db = await get_db()
    users = await db.fetchall("SELECT * from leaderboard;")
    print(users)
    
async def refresh_leaderboards():
    db = await get_db()
    users = list(await db.fetchall("SELECT pp, user_id from accounts;"))
    users.sort(reverse=True)
    for i, u in enumerate(users, start=1):
        await db.execute("INSERT INTO `leaderboard` (`position`, `user_id`) VALUES (%s, %s);", (i, u[1]))