from globals import sql

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
        """
        self
class AccountNew:
    """A significantly improved version of the account object, representing 
    a singular user."""

    def __init__(self):
        """Creates placeholders """
