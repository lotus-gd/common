from common.globals import sql
from common.objects.account import Account
from common.objects.privilege import PrivilegeGroup

def safe_name(name: str) -> str:
    """Creates a safe variant of the username. The safe name is:
            - RStripped
            - Lower case
            - Spaces replaced with underscores.
    
    Args:
        name (str): The name to be converted into a safe variant.
    """

    return name.rstrip().lower().replace(" ", "_")

async def get_user(id: int) -> Account:
    """Fetches user by id (shorthand for Account.from_sql(id))
    
    Note:
        Please use `Account.from_sql` whenever you can as it is significantly
            faster.
    
    Args:
        id (int): The ID of a user
    """

    return await Account.from_sql(id)

async def get_total_users() -> int:
    users = await sql.fetchall(
        "SELECT id FROM users"
    )
    return len(users)

async def get_all_users(limit=10):
    userlist = []
    users = await sql.fetchall(
        "SELECT id FROM users"
    )
    users = list(users)
    users.reverse()
    for i, user in enumerate(users):
        user = user[0]
        if i < limit+1:
            acc = await Account.from_sql(user)
            userlist.append(acc)
    return userlist 

async def get_user_by_name(name: str) -> Account:
    """Fetches an account object by searching for a name.
    
    Note:
        Please use `Account.from_sql` whenever you can as it is significantly
            faster.
    
    Args:
        name (str): The user's name.
    """

    # We fetch ID from name.
    user_id_db = await sql.fetchone(
        "SELECT id FROM users WHERE safe_name = %s LIMIT 1",
        (safe_name(name),)
    )
    if not user_id_db: return

    return await Account.from_sql(user_id_db[0])

async def get_badges():
    badgelist = []
    badges = await sql.fetchall(
        "SELECT id FROM badges"
    )
    badges = list(badges)
    badges.reverse()
    for badge in badges:
        badge = badge[0]
        temp = await Account.from_sql(badge)
        badgelist.append(temp)
    return badgelist 