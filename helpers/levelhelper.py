import gd
from common.objects.level import Level
from common.globals import sql

async def get_level():
    pass

async def get_level_by_name():
    pass

async def get_total_levels():
    levels = await sql.fetchall(
        "SELECT id FROM levels"
    )
    return len(levels)

async def database_level(level_id: int):
    """
    Database level from robs servers using gd.py
    """
    client = gd.Client()
    levels = await client.get_level(level_id)
    for l in levels:
        if isinstance(l.difficulty, gd.DemonDifficulty):
            demon_difficulty = l.difficulty.value
            difficulty = 10
        else:
            difficulty = l.difficulty
            demon_difficulty = 0
            
        if not l.password:
            password = 0
        else:
            password = l.password
        
        lvl = await Level.database(l.id, l.name, l.description, l.version, l.downloads,
                       l.rating, l.score, l.creator.name, l.song.id, difficulty,
                       demon_difficulty, password, l.stars, l.coins, l.uploaded_timestamp,
                       l.length.value, l.object_count)