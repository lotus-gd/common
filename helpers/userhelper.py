from common.db.mysql import get_db
from common.config import config
from common.objects.account import Account

async def get_user(id: int):
    db = await get_db()
    user = await db.fetchall("SELECT * from accounts WHERE user_id = %s;", id)
    user = user[0]
    return Account(
        username=user[0],
        email=user[2],
        is_admin=user[4],
        user_id=user[5],
        youtube=user[6],
        twitter=user[7],
        twitch=user[8],
        discord=user[9],
        register_date=user[11],
        privileges=user[12],
        is_bot=user[13],
        stars=user[14],
        demons=user[15],
        color1=user[16],
        color2=user[17],
        icon_type=user[18],
        coins=user[19],
        user_coins=user[20],
        icon=user[21],
        ship=user[22],
        ball=user[23],
        bird=user[24],
        dart=user[25],
        robot=user[26],
        glow=user[27],
        cp=user[28],
        ip=user[30],
        last_played=user[31],
        diamonds=user[32],
        orbs=user[33],
        completed_levels=user[34],
        spider=user[35],
        explosion=user[36],
        banned=user[37],
        pp=user[38]
    )

async def get_user_by_name(name: str):
    db = await get_db()
    user = await db.fetchall("SELECT * from accounts WHERE username = %s;", name)
    user = user[0]
    return Account(
        username=user[0],
        email=user[2],
        is_admin=user[4],
        user_id=user[5],
        youtube=user[6],
        twitter=user[7],
        twitch=user[8],
        discord=user[9],
        register_date=user[11],
        privileges=user[12],
        is_bot=user[13],
        stars=user[14],
        demons=user[15],
        color1=user[16],
        color2=user[17],
        icon_type=user[18],
        coins=user[19],
        user_coins=user[20],
        icon=user[21],
        ship=user[22],
        ball=user[23],
        bird=user[24],
        dart=user[25],
        robot=user[26],
        glow=user[27],
        cp=user[28],
        ip=user[30],
        last_played=user[31],
        diamonds=user[32],
        orbs=user[33],
        completed_levels=user[34],
        spider=user[35],
        explosion=user[36],
        banned=user[37],
        pp=user[38]
    )