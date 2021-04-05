# All of Lotus' shared constants.

class Privileges: # Should I use IntFlag?
    """All of Lotus' privilege enum. These are all bitwise numbers."""

    LOGIN          = 1 << 1 # This missing is ban
    PUBLIC         = 1 << 2 # This missing is restriction.
    SUPPORTER      = 1 << 3
    MANAGE_LEVELS  = 1 << 4
    MANAGE_REPLAYS = 1 << 5
    MANAGE_USERS   = 1 << 6
    DEVELOPER      = 1 << 7

class RankingType:
    """Ranking statuses for a level, which determine multiple factors such as
    whether PP should be awarded."""

    UNRANKED  = 0
    RATED     = 1
    CHALLENGE = 2
    RANKED    = 3
