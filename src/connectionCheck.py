import mariadb
import os
import sys


def checkConnection(fun):

    def connWrap(self, *args, **kwargs):
        alreadyConnected = True
        if self._connection is None:
            alreadyConnected = False
            self._connection = mariadb.connect(
                user=os.getenv("DBUSERNAME"),
                password=os.getenv("DBUSERPASS"),
                database=os.getenv("DBNAME"),
                host=os.getenv("DBHOST"))

        return_value = fun(self, *args, **kwargs)

        if not alreadyConnected:
            self._connection.close()
            self._connection = None

        return return_value

    return connWrap
