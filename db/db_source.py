from operator import truediv

import sqlalchemy as sa
from sqlalchemy import create_engine


class DbConnexion:

    def __init__(self, connexion_string):
        self._connexion_string = connexion_string
        self._connection_url = None
        self._engine = None

        self._set_connexion_url()
        self._set_engine()

    def _set_connexion_url(self):
        try:
            self._connection_url = sa.engine.URL.create(
                drivername=self._connexion_string["DRIVER_NAME"],
                username=self._connexion_string["USERNAME"],
                password=self._connexion_string["PASSWORD"],
                host=self._connexion_string["SERVER"],
                database=self._connexion_string["DATABASE"],
                query={
                    "driver": "ODBC Driver 17 for SQL Server",
                    "autocommit": "True",
                }
            )
            return True
        except Exception(ConnectionAbortedError) as e:
            print("Error connecting to DB:",e)
            return False

    def _set_engine(self):
        if self._connection_url is not None:
            self._engine = create_engine(self._connection_url).execution_options(
                isolation_level="AUTOCOMMIT"
            )

    @property
    def engine(self):
        return self._engine