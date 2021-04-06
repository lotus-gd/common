# The privilege group object.
from common.constants import Privileges

class PrivilegeGroup:
    """An object representing a group of users with the same privileges."""

    def __init__(self) -> None:
        """Sets the placeholders for the privilege group. Please use the
        classmethods instead."""

        self.name: str = ""
        self.description: str = ""
        self.privileges: int = 0
    
    def has_privilege(self, priv: Privileges) -> bool:
        """Checks if the current privilege group has the privilege to do
        `priv`.
        
        Args:
            priv (Privileges): The privilege to check for.
        
        Returns:
            `bool` corresponding to the presence of the privilege.
        """

        return bool(self.privileges & priv)
