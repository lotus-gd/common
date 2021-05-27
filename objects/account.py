from common.helpers.crypt import bcrypt_check, bcrypt_hash
from common.globals import sql, user_cache, privilege_cache
from typing import List
from common.constants import Privileges
from .privilege import PrivilegeGroup
import time

class Badge:
    """Object representing a singular badge."""

    def __init__(self, badge_id: int) -> None:
        """
        Args:
            badge_id (int): The SQL database ID of the badge."""
        self.id = badge_id
        self.title: str = ""
        self.description: str = ""
        self.colour: str = ""
        self.name: str = "" # Internal name ig??
    
    async def load_sql(self) -> None:
        """Loads the badge data directly from the MySQL database."""

        badge_db = await sql.fetchone(
            "SELECT title, description, colour, name FROM badges WHERE "
            "id = %s LIMIT 1",
            (self.id,)
        )
        if badge_db is None: return

        (
            self.title,
            self.description,
            self.colour,
            self.name
        ) = badge_db
    
    async def insert(self) -> None:
        """Inserts the badge into the MySQL database.
        
        Note:
            This also sets the `id` attribute in the object based on
                `cur.lastrowid`.
        """

        # Check if it already has an ID (already exists.)
        if self.id: return

        self.id = await sql.execute(
            "INSERT INTO badges (title, description, colour, name) "
            "VALUES (%s,%s,%s,%s)",
            (self.title, self.description, self.colour, self.name)
        )
    
    async def save(self) -> None:
        """Saves the current state of the badge (title, desc etc) from the
        attribute values to the MySQL database."""

        # No id = we cant save. Maybe raise exception?
        if not self.id: return

        await sql.execute(
            "UPDATE badges SET title=%s, description=%s, colour=%s, name=%s "
            "WHERE id = %s LIMIT 1",
            (self.title, self.description, self.colour, self.name)
        )
    
    @classmethod
    async def from_sql(cls, badge_id: int):
        """Creates an instance of `Badge` from data in MySQL.
        
        Args:
            badge_id (int): The ID of the badge in the `badges` table.
        
        Returns:
            Instance of `Badge`.
        """

        badge = cls(badge_id)
        await badge.load_sql()
        return badge

class Stats:
    """Object representing the user's in-game stats."""

    def __init__(self, user_id: int) -> None:
        """Creates the stats object.
        
        Args:
            user_id (int): The ID of the user located within the database.
        """
        self._user_id: int = user_id
        
        # Actual stats.
        self.pp: float = 0
        self.stars: int = 0
        self.coins: int = 0
        self.u_coins: int = 0
        self.demons: int = 0
        self.attempts: int = 0

        # Icons
        self.display_icon: int = 0
        self.icon: int = 0
        self.ship: int = 0
        self.ufo: int = 0
        self.ball: int = 0
        self.robot: int = 0
        self.spider: int = 0

        # Ranking
        self.country_rank: int = 0
        self.global_rank: int = 0
    
    async def recalc_pp(self) -> None:
        """Recalculates the user's total pp considering weighing from scratch
        using submitted scores.
        
        Note:
            This DOES NOT update the value stored in the DB. For that you will
                need to manually run the `save` coro.
        """

        # Scores not done.
        ...
    
    async def calculate_rank(self) -> None:
        """Calculates the user's global and country rank."""

        # TODO: Restrict/ban check (once privileges are storted out)
        # Set both to 0 if WE are restricted.

        glob_rank_db = await sql.fetchone(
            "SELECT COUNT(*) FROM users WHERE pp > %s AND privileges & %s",
            (self.pp, Privileges.PUBLIC)
        )

        self.global_rank = glob_rank_db[0] + 1

        # TODO: Country ranks

    
    async def load_sql(self) -> None:
        """Loads the user's statistics from the MySQL database."""

        stats_db = await sql.fetchone(
            "SELECT pp, stars, coins, u_coins, demons, display_icon, icon, "
            "ship, ufo, ball, robot, spider, attempts FROM users WHERE "
            "id = %s LIMIT 1",
            (self._user_id,)
        )

        if not stats_db: return

        (
            self.pp,
            self.stars,
            self.coins,
            self.u_coins,
            self.demons,
            self.display_icon,
            self.icon,
            self.ship,
            self.ufo,
            self.ball,
            self.robot,
            self.spider,
            self.attempts
        ) = stats_db

        await self.calculate_rank()
    
    # NOTE: We might need some boomlings interaction here, such as stats
    # updates or initial user stats stuff.
    
    async def save(self) -> None:
        """Saves the current statistic attributes in the MySQL database."""

        # We need an ID to save to.
        if not self._user_id: return

        await sql.execute(
            "UPDATE users SET pp=%s, stars=%s, coins=%s, u_coins=%s, demons=%s,"
            "display_icon=%s, icon=%s, ship=%s, ufo=%s, ball=%s, robot=%s,"
            "spider=%s, attempts=%s WHERE id = %s LIMIT 1",
            (
                self.pp, self.stars, self.coins, self.u_coins, self.demons,
                self.display_icon, self.icon, self.ship, self.ufo, self.ball,
                self.robot, self.spider, self.attempts, self._user_id
            )
        )

class Account:
    """A significantly improved version of the account object, representing 
    a singular user."""

    def __init__(self, user_id: int):
        """Configures the defaults for the account object.
        
        Args:
            user_id (int): The ID of the user.
        """

        # Stuff
        self.name: str = ""
        self.id: int = user_id
        self.email: str = ""
        self.password_hash: str = "" # Idk whether to store it here... but oh well
        self.stats: Stats = Stats(user_id)
        self.register_ts: int = 0
        self.last_active_ts: int = 0
        self.country: str = "XX" # 2 letter upper.
        self.pp = 0

        # Extra stuff
        self.badges: List[Badge] = []
        self.privilege_group: PrivilegeGroup = None
    
    @property
    def safe_name(self) -> str:
        """Creates a 'safe' version of the name used for quick lookups. The
        safe name is:
            - RStripped
            - Lower case
            - Spaces replaced with underscores.
        """

        return self.name.rstrip().lower().replace(" ", "_")
    
    async def load(self, full: bool = True) -> None:
        """Loads the user data directly from the database.
        
        Args:
            full (bool): Whether 'optional' data should be loaded too (eg
                badges)
        """

        # SQL STUFF!!
        user_db = await sql.fetchone(
            "SELECT name, email, password, register_ts, last_active_ts, "
            "privileges, country FROM users WHERE id = %s LIMIT 1",
            (self.id,)
        )
        if not user_db: return

        # Set vars.
        (
            self.name,
            self.email,
            self.password_hash,
            reg_ts, # We have to convert the type
            l_a_ts, # We have to convert the type
            priv, # We need some priv group logic.
            self.country
        ) = user_db
        
        # Type conversion.
        self.register_ts = int(reg_ts)
        self.last_active_ts = int(l_a_ts)

        self.privilege_group = privilege_cache.get(priv)

        await self.stats.load_sql()

        if full:
            await self.set_badges()
    
    async def set_badges(self) -> None:
        """Loads the assigned badges from database and sets their objects in
        the badges list."""

        # TODO: Look into caching this as it really should be.
        self.badges.clear()

        self.badges = [
            await Badge.from_sql(b_id[0])
            for b_id in await sql.fetchall(
                "SELECT badge_id FROM badge_assign WHERE user_id = %s",
                (self.id,)
            )
        ]
    
    async def save(self) -> None:
        """Saves the current user attributes in the MySQL database."""

        if not self.id: return

        await sql.execute(
            "UPDATE users SET name=%s, email=%s, password=%s, register_ts,"
            "last_active_ts=%s, country=%s WHERE id = %s LIMIT 1",
            (
                self.name, self.email, self.password_hash, self.register_ts,
                self.last_active_ts, self.country, self.id
            )
        )
    
    async def update_last_active(self) -> None:
        """Sets the last active time to the current timestamp."""

        self.last_active_ts = int(time.time())

        # We set in db!
        await sql.execute(
            "UPDATE users SET last_active_ts = %s WHERE id = %s LIMIT 1",
            (self.last_active_ts, self.id)
        )

    async def set_privilege_group(self, group: PrivilegeGroup) -> None:
        """Sets the user's current privilege group in the database."""

        self.privilege_group = group

        await sql.execute(
            "UPDATE users SET privileges = %s WHERE id = %s LIMIT 1",
            (group.privileges, self.id)
        )
    
    def compare_pass(self, plain_pass: str) -> bool:
        """Compares a plaintext using bcrypt to the user's password hash.
        
        Args:
            plain_pass (str): A plaintext password to compare the hash
                against.
        
        Returns:
            `bool` corresponding to the passwords matching.
        """

        # TODO: Look into caching this as bcrypt by nature is slow.

        return bcrypt_check(plain_pass, self.password_hash)
    
    def cache(self) -> None:
        """Caches the user in a global cache for rapid future access."""

        if not self.id: return
        user_cache.cache(self.id, self)
    
    @classmethod
    async def from_sql(cls, user_id: int):
        """Creates an instance of `Account` using data from the MySQL database.
        
        Args:
            user_id (int): The ID of the user in the database.
        """

        usr = cls(user_id)
        await usr.load(True)
        return usr
    
    @classmethod
    async def from_id(self, user_id: int):
        """Fetches an instance of Account matching `user_id`.
        
        Note:
            This does multiple lookups for the user in order of speed,
                checking the cache first and if not found proceeding
                to check the MySQL database. It also automatically
                caches the object for future use.
        
        Args:
            user_id (int): The ID of the user in the database.
        """

        # Check cache for really speedy returns.
        if u_cache := user_cache.get(user_id): return u_cache

        # We need to use the db.
        u_db = await Account.from_sql(user_id)
        # Cache it for later SPEED.
        if u_db is not None: user_cache.cache(u_db.id, u_db)
        return u_db
    
    @classmethod
    async def register(cls, name: str, password: str, email: str, ip: str):
        """Creates a new user in the database and returns an instance of
        `Account` for that user.
        
        Args:
            name (str): The username of the user.
            password (str): The plaintext password for the user.
            email (str): The email associated with the user.
            ip (str): The IP of the user (used for geolocation).
        """

        # This will seriously mess up safe name lookups.
        if "_" in name and " " in name:
            raise ValueError(
                "A username may not contain spaces and underscores"
            )

        # We cant import safe username func here as CIRCULAR IMPORTS.
        safe_name = name.rstrip().lower().replace(" ", "_")

        # Check if they already exist.
        exists = await sql.fetchone(
            "SELECT 1 FROM users WHERE safe_name = %s OR email = %s LIMIT 1",
            (safe_name, email)
        )

        if exists:
            raise Exception(
                "A user with that name or email already exists."
            )

        # Hash password
        password_hash = bcrypt_hash(password)
        register_ts = int(time.time())

        # TODO: IP geoloc.
        country = "XX"

        # Insert them.
        u_id = await sql.execute(
            "INSERT INTO users (name, safe_name, email, password, register_ts,"
            "last_active_ts, country) VALUES (%s,%s,%s,%s,%s,%s,%s)",
            (name, safe_name, email, password_hash, register_ts, register_ts,
            country)
        )

        return await Account.from_sql(u_id)
