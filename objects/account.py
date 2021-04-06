from dataclasses import dataclass

@dataclass
class Account:
    username: str = ""
    email: str = ""
    account_id: int = 0
    register_date: int = 0
    privileges: int = 0
    stars: int = 0
    demons: int = 0
    icon: int = 0
    color1: int = 0
    color2: int = 0
    icon_type: int = 0
    coins: int = 0
    user_coins: int = 0
    ship: int = 0
    ball: int = 0
    wave: int = 0
    robot: int = 0
    glow: bool = False
    cp: int = 0
    diamonds: int = 0
    orbs: int = 0
    spider: int = 0
    explosion: int = 0
    banned: bool = False
    youtube: str = ""
    twitter: str = ""
    twitch: str = ""
    pp: int = 0