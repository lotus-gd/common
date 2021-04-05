from dataclasses import dataclass

@dataclass
class LeaderboardScore:
    username: str
    date: int
    place: int # pos on leaderboard (change later)