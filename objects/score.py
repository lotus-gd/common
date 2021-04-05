from dataclasses import dataclass

@dataclass
class LeaderboardScore:
    username: str = ""
    date: int = 0
    place: int = 0# pos on leaderboard (change later)