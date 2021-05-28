# The privilege group object.
from common.constants import Privileges
from common.globals import sql

class PrivilegeGroup:
    """An object representing a group of users with the same privileges."""

    def __init__(self) -> None:
        """Sets the placeholders for the privilege group. Please use the
        classmethods instead."""

        self.id = 0
        self.name: str = ""
        self.description: str = ""
        self.privileges: int = 0
        
    async def load(self):
        priv_group_db = await sql.fetchone(
            "SELECT id, name, description, privileges FROM users WHERE id = %s LIMIT 1",
            (self.id,)
        )
        if not priv_group_db: return

        (
            self.id,
            self.name,
            self.description,
            self.privileges
        ) = priv_group_db
    
    @classmethod
    async def from_sql(cls, priv_id: int):
        priv = cls(priv_id)
        await priv.load()
        return priv
    
    def has_privilege(self, priv: Privileges) -> bool:
        """Checks if the current privilege group has the privilege to do
        `priv`.
        
        Args:
            priv (Privileges): The privilege to check for.
        
        Returns:
            `bool` corresponding to the presence of the privilege.
        """

        return bool(self.privileges & priv)
