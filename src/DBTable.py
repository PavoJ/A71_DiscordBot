from DBHandler import DBHandler


class DBTable(DBHandler):
    def __init__(self, table_name):
        DBHandler.__init__(self)
        self._table_name = table_name

    def getTableName(self):
        return self._table_name

    def getEntry(self, **values):
        return DBHandler.getEntry(self, self._table_name, **values)

    def getEntries(self, **values):
        return DBHandler.getEntries(self, self._table_name, **values)

    def changeEntry(self, idname, id, colname, colvalue) -> bool:
        return DBHandler.changeEntry(self, self._table_name, idname, id, colname, colvalue)

    def getTable(self):
        return DBHandler.getTable(self, self._table_name)

    def addEntry(self, colnames, entries):
        return DBHandler.addEntry(self, self._table_name, colnames, entries)

