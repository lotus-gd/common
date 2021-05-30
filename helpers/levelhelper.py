import gd
from common.objects.level import Level

async def get_level():
    pass

async def get_level_by_name():
    pass

async def database_level():
    """
    Database level from robs servers using gd.py
    """
    client = gd.Client()
    levels = await client.search_levels(filters=gd.Filters(demon_difficulty=gd.DemonDifficulty.EXTREME_DEMON), pages=range(34))
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