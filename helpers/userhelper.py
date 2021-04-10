from common.globals import connect_sql, sql, connected
from common.objects.account import Account

async def get_user(id: int) -> Account:
    if not connected:
        await connect_sql()
    user = await sql.fetchall("SELECT * from accounts WHERE user_id = %s;", id)
    user = user[0]
    acc = Account(user[5])
    acc.username =  user[0]
    acc.email = user[2]
    acc.is_admin = user[4]
    acc.youtube = user[6]
    acc.twitter = user[7]
    acc.twitch = user[8]
    acc.discord = user[9]
    acc.register_date = user[11]
    acc.privileges = user[12]
    acc.is_bot = user[13]
    acc.stars = user[14]
    acc.demons = user[15]
    acc.color1 = user[16]
    acc.color2 = user[17]
    acc.icon_type = user[18]
    acc.coins = user[19]
    acc.user_coins = user[20]
    acc.icon = user[21]
    acc.ship = user[22]
    acc.ball = user[23]
    acc.bird = user[24]
    acc.dart = user[25]
    acc.robot = user[26]
    acc.glow = user[27]
    acc.cp = user[28]
    acc.ip = user[30]
    acc.last_played = user[31]
    acc.diamonds = user[32]
    acc.orbs = user[33]
    acc.spider = user[35]
    acc.explosion = user[36]
    acc.banned = user[37]
    acc.pp = user[38]
    return acc

async def get_user_by_name(name: str) -> Account:
    if not connected:
        await connect_sql()
    user = await sql.fetchall("SELECT * from accounts WHERE username = %s;", name)
    user = user[0]
    acc = Account(user[5])
    acc.username =  user[0]
    acc.email = user[2]
    acc.is_admin = user[4]
    acc.youtube = user[6]
    acc.twitter = user[7]
    acc.twitch = user[8]
    acc.discord = user[9]
    acc.register_date = user[11]
    acc.privileges = user[12]
    acc.is_bot = user[13]
    acc.stars = user[14]
    acc.demons = user[15]
    acc.color1 = user[16]
    acc.color2 = user[17]
    acc.icon_type = user[18]
    acc.coins = user[19]
    acc.user_coins = user[20]
    acc.icon = user[21]
    acc.ship = user[22]
    acc.ball = user[23]
    acc.bird = user[24]
    acc.dart = user[25]
    acc.robot = user[26]
    acc.glow = user[27]
    acc.cp = user[28]
    acc.ip = user[30]
    acc.last_played = user[31]
    acc.diamonds = user[32]
    acc.orbs = user[33]
    acc.spider = user[35]
    acc.explosion = user[36]
    acc.banned = user[37]
    acc.pp = user[38]
    return acc