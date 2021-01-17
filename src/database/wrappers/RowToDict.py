import mariadb
from database import StaticConnection

#converts a mariadb.Row in a list of dictionaries
def _RowToDict(rows, cols): 
    print(cols)
    retDict = {}
    for v in rows:
        if str(type(v)) == "<class 'mariadb.Row'>":
            retDict[rows.index(v)] = _RowToDict(v)
        else:
            print(dir(row))
            retDict[row] = v
    
    print(retDict)
    return retDict

#wrapper to the _RowToDict(row) function
def RowToDict(fun):
    def wrap(self, tablename, *args, **kwargs):

        cur = StaticConnection.connection.cursor()
        cur.execute(f'SHOW COLUMNS FROM {tablename}')
        cols = cur.fetchall()
        cur.close

        rows = fun(self, tablename, *args, **kwargs)

        return _RowToDict(rows, cols)

    return wrap
