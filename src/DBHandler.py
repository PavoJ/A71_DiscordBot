import mariadb
from dotenv import load_dotenv
import os

load_dotenv()

class DBHandler:
    def __init__(self):
        self.__connection = mariadb.connect(
            user     = os.getenv("DBUSER"),
            password = os.getenv("DBUSERPASS"),
            database = os.getenv("DBNAME"),
            host     = os.getenv("DBHOST"))

        self.__cursor = self.__connection.cursor()
        self.__cursor.execute("SELECT * FROM menu")
        print(self.__cursor.fetchall())

        return

    def __del__(self):
        self.__cursor.close()
        self.__connection.close()
        return

    def getEntry(self):
        pass

    def addEntry(self):
        pass

    def remEntry(self):
        pass
