import mariadb
from dotenv import load_dotenv

from database import StaticConnection
from database.wrappers.RowToNamedTuple import RowToNamedTuple



load_dotenv()


class DBHandler:
    def __init__(self):
        self._connection = StaticConnection.connection
        pass

    def __del__(self):
        return

    def _rawGetEntry(self, tablename, **values):
        cur = self._connection.cursor()#named_tuple=True)

        to_search = ""
        cnt = 1

        for col, val in values.items():
            to_search = to_search + f"{col}='{val}'"
            if cnt != len(values):
                to_search = to_search + " AND "
            cnt = cnt + 1

        try:
            cur.execute(f"SELECT * FROM {tablename} WHERE {to_search};")
        except mariadb.Error as e:
            print(f"error: {e}")
            cur = None

        return cur

    @RowToNamedTuple
    def getEntry(self, tablename, **values):
        cur = self._rawGetEntry(tablename, **values)
        ret = None

        if cur is not None:
            ret = cur.fetchone()
            cur.close()

        return ret

    @RowToNamedTuple
    def getEntries(self, tablename, **values):
        cur = self._rawGetEntry(tablename, **values)
        
        ret = cur.fetchall()
        cur.close()

        return ret

    # changes an existing entry
    def changeEntry(self, table_name, idname, id, colname, colvalue) -> bool:
        found_entry = DBHandler.getEntry(self, table_name, **{idname: id}) is not None

        if found_entry:
            cur = self._connection.cursor()
            cur.execute(f"UPDATE {table_name} SET {colname}={colvalue} WHERE {idname}={id}")

            self._connection.commit()

        return found_entry

    @RowToNamedTuple
    def getTable(self, table_name):
        cur  = self._connection.cursor(named_tuple=True)
        cur.execute(f"SELECT * FROM {table_name}")

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

        has_failed = False
        try:
            cur.execute(f"INSERT INTO {tablename} ({parsed_entry_types}) VALUES ({parsed_entry})")
        except mariadb.IntegrityError as e:
            print(e)
            has_failed = True

        self._connection.commit()
        cur.close()

        kwargs = {}
        for colC in range(len(colnames)):
            kwargs[colnames[colC]] = entries[colC]

        if has_failed:
            return None
        else:
            return DBHandler.getEntry(self, tablename, **kwargs)

    # not implemented yet
    def remEntry(self):
        pass
