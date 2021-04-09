from globals import sql
from typing import List
from constants import Privileges
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
            "ship, ufo, ball, robot, spider FROM users WHERE id = %s LIMIT 1",
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
            self.spider
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
            "spider=%s WHERE id = %s LIMIT 1",
            (
                self.pp, self.stars, self.coins, self.u_coins, self.demons,
                self.display_icon, self.icon, self.ship, self.ufo, self.ball,
                self.robot, self.spider, self._user_id
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
        self.id: int = 0
        self.email: str = ""
        self.password_hash: str = "" # Idk whether to store it here... but oh well
        self.stats: Stats = Stats(user_id)
        self.register_ts: int = 0
        self.last_active_ts: int = 0
        self.country: str = "XX" # 2 letter upper.

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

        # TODO: Privilege group logic

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
    
    @classmethod
    async def from_sql(cls, user_id: int):
        """Creates an instance of `Account` using data from the MySQL database.
        
        Args:
            user_id (int): The ID of the user in the database.
        """

        usr = cls(user_id)
        await usr.load(True)
        return usr
