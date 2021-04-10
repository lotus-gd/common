from common.globals import connect_sql, sql, connected
from common.objects.account import Account

def safe_name(name: str) -> str:
    """Creates a safe variant of the username. The safe name is:
            - RStripped
            - Lower case
            - Spaces replaced with underscores.
    
    Args:
        name (str): The name to be converted into a safe variant.
    """

    return name.rstrip().lower().replace(" ", "_")

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