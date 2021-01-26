import mariadb
from database import StaticConnection
from collections import namedtuple

#converts a mariadb.Row in a list of dictionaries
def _RowToNamedTuple(rows, cols): 
    if rows is None or len(rows)==0:
        return list()
    ntuple = namedtuple("dbrow", cols)
    
    ret = list()
    convert = False

   
    for v in rows:  
        if type(v) is tuple:
            convert = False
            ret.append(_RowToNamedTuple(v, cols))
        else:
            convert = True
            ret.append(v)
    
    if not convert:
        return ret
    else: #if it's a tuple (there is only one row to parse)
        return ntuple._make(ret)

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

        rows = fun(self, tablename, *args, **kwargs)
       
        return _RowToNamedTuple(rows, cols)

    return wrap
