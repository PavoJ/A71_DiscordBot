import mariadb
from dotenv import load_dotenv
import os

load_dotenv()

class DBHandler:
    def __init__(self):
        self._connection = mariadb.connect(
            user     = os.getenv("DBUSERNAME"),
            password = os.getenv("DBUSERPASS"),
            database = os.getenv("DBNAME"),
            host     = os.getenv("DBHOST"))

        return

    def __del__(self):
        self._connection.close()
        return

    def getConnection(self):
        return self._connection

    def getEntry(self, tableName, entryName, name):
        cur = self._connection.cursor(named_tuple=True)
        cur.execute(f"SELECT * FROM {tableName} WHERE {entryName}={name} LIMIT 1; ")

        ret = cur.fetchone()
        cur.close()
        return ret

    def changeEntry(self, table, idName, id, colName, colValue):
        cur = self._connection.cursor()
        cur.execute(f"UPDATE {table} SET {colName}={colValue} WHERE {idName}={id}")

        self._connection.commit()
        return

    def getTable(self, tableName) -> int:
        cur  = self._connection.cursor(named_tuple=True)
        cur.execute(f"SELECT * FROM {tableName}")

        ret = cur.fetchall()

        cur.close()
        return ret

    '''
        adds an entry to the specified table, containing entries labeled colNames. Returns the added entry
        CAREFUL: for addEntry to return the added entry, the first colName entries pair must be unique
    '''
    def addEntry(self, tableName, colNames, entries):
        cur = self._connection.cursor()

        parsedEntry = ""
        parsedEntryTypes = ""

        cnt = 0
        for x in range(0, len(entries)):
            cnt = cnt+1
            parsedEntry      = parsedEntry      + f"'{entries[x]}'"
            parsedEntryTypes = parsedEntryTypes + f"{colNames[x]}"

            if x != len(entries)-1:
                parsedEntry = parsedEntry+", "
                parsedEntryTypes = parsedEntryTypes+", "

        cur.execute(f"INSERT INTO {tableName} ({parsedEntryTypes}) VALUES ({parsedEntry})")
        self._connection.commit()
        cur.close()

        return self.getEntry(tableName, colNames[0], entries[0])

    def remEntry(self):
        pass
