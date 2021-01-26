import mariadb
from database import StaticConnection
from collections import namedtuple

#converts a mariadb.Row in a list of dictionaries
def _RowToNamedTuple(rows, cols): 
    ntuple = namedtuple("dbrow", cols)
    ret = None
    
    for v in rows:
        if str(type(v)) == "<class 'mariadb.Row'>":
            if ret is None:
                ret = list()
            ret.append(_RowToNamedTuple(v, cols))
        else:
            if ret is None:
                ret = list()
            ret.append(v)
    
    print(ret)
    if type(ret) is list:
        return ret
    else: #if it's a tuple (there is only one row to parse)
        return ntuple._make(*ret)

#wrapper to the _RowToDict(row) function
def RowToNamedTuple(fun):
    def wrap(self, tablename, *args, **kwargs):

        cur = StaticConnection.connection.cursor()
        cur.execute(f'SHOW COLUMNS FROM {tablename}')
        raw_cols = cur.fetchall()
        cur.close
        
        cols = list()
        for col in raw_cols:
            cols.append(col[0])
        print(" ".join(cols))

        rows = fun(self, tablename, *args, **kwargs)

        return _RowToNamedTuple(rows, cols)

    return wrap
