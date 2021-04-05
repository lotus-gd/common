from dataclasses import dataclass

@dataclass
class Score:
    username: str
    date: int
    place: int # pos on leaderboard (change later)