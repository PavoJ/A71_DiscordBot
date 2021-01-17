import mariadb
import os
from dotenv import load_dotenv

load_dotenv()

connection = mariadb.connect(
    user=os.getenv("DBUSERNAME"),
    password=os.getenv("DBUSERPASS"),
    database=os.getenv("DBNAME"),
    host=os.getenv("DBHOST")
)
connection.auto_reconnect = True
