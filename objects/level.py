from common.globals import sql

class Level:

    def __init__(self, level_id: int):
        self.id: int = level_id
        self.name: str = ""
        self.description: str = ""
        self.version: int = 0
        self.downloads: int = 0
        self.rating: int = 0
        self.score: int = 0
        self.creator: str = ""
        self.song_id: int = 0
        self.difficulty: int = 0
        self.demon_difficulty: int = 0
        self.password: int = 0
        self.rob_stars: int = 0
        self.coins: int = 0
        self.uploaded_timestamp: int = 0
        self.length: int = 0
        self.objects: int = 0
    
    async def load(self) -> None:
        user_db = await sql.fetchone(
            "SELECT id, name, description, version, downloads, rating, "
            "score, creator, song_id, difficulty, demon_difficulty,"
            "password, rob_stars, coins, uploaded_timestamp, length,"
            "objects FROM users WHERE id = %s LIMIT 1",
            (self.id,)
        )
        if not user_db: return

        (
            self.id,
            self.name,
            self.description,
            self.version,
            self.downloads,
            self.rating,
            self.creator,
            self.song_id,
            self.difficulty,
            self.demon_difficulty,
            self.password,
            self.rob_stars,
            self.coins,
            self.uploaded_timestamp,
            self.length,
            self.objects
        ) = user_db
    
    async def save(self) -> None:
        if not self.id: return
        
        await sql.execute(
            "UPDATE users SET name=%s, description=%s, version=%s, downloads=%s,"
            "rating=%s, creator=%s, song_id=%s, difficulty=%s, demon_difficulty=%s,"
            "password=%s, rob_stars=%s, coins=%s, uploaded_timestamp=%s,"
            "length=%s, objects=%s WHERE id = %s LIMIT 1",
            (
                self.name, self.description, self.version, self.downloads,
                self.rating, self.creator, self.song_id, self.difficulty,
                self.demon_difficulty, self.password, self.rob_stars, self.coins,
                self.uploaded_timestamp, self.length, self.objects, self.id
            )
        )
    
    @classmethod
    async def from_sql(cls, level_id: int):

        lvl = cls(level_id)
        return lvl
    
    @classmethod
    async def from_id(self, user_id: int):
        lvl = await Level.from_sql(user_id)
        return lvl