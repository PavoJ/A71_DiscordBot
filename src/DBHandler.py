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

    def getEntry(self, tablename, entryname, name):
        cur = self._connection.cursor(named_tuple=True)
        cur.execute(f"SELECT * FROM {tablename} WHERE {entryname}={name} LIMIT 1;")

        ret = cur.fetchone()
        cur.close()
        return ret

    def changeEntry(self, table, idname, id, colname, colvalue):
        cur = self._connection.cursor()
        cur.execute(f"UPDATE {table} SET {colname}={colvalue} WHERE {idname}={id}")

        self._connection.commit()
        return

    def getTable(self, tablename) -> int:
        cur  = self._connection.cursor(named_tuple=True)
        cur.execute(f"SELECT * FROM {tablename}")

        ret = cur.fetchall()

        cur.close()
        return ret

    '''
        adds an entry to the specified table, containing entries labeled colNames. Returns the added entry
        CAREFUL: for addEntry to return the added entry, the first colName entries pair must be unique
    '''
    def addEntry(self, tablename, colnames, entries):
        cur = self._connection.cursor()

        parsed_entry = ""
        parsed_entry_types = ""

        cnt = 0
        for x in range(0, len(entries)):
            cnt = cnt+1
            parsed_entry      = parsed_entry      + f"'{entries[x]}'"
            parsed_entry_types = parsed_entry_types + f"{colnames[x]}"

            if x != len(entries)-1:
                parsed_entry = parsed_entry+", "
                parsed_entry_types = parsed_entry_types+", "

        cur.execute(f"INSERT INTO {tablename} ({parsed_entry_types}) VALUES ({parsed_entry})")
        self._connection.commit()
        cur.close()

        return self.getEntry(tablename, colnames[0], entries[0])

    def remEntry(self):
        pass
