import mariadb
import os

class StaticConnection:
    connection = None

    @staticmethod
    def initialize_connection():
        connection = mariadb.connect(
            user=os.getenv("DBUSERNAME"),
            password=os.getenv("DBUSERPASS"),
            database=os.getenv("DBNAME"),
            host=os.getenv("DBHOST")
        )