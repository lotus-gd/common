# Idk what to do so i will just make a botch attempt to solve this.
from common.db.mysql import MySQLPool
from common.config import config

sql = MySQLPool()

async def connect_sql():
    await sql.connect(
        config["db_host"],
        config["db_user"],
        config["db_password"],
        config["db_database"],
        config["db_port"]
    )
