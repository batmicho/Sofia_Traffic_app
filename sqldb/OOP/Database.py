import sqlite3


class Database:
    con = None
    database = None

    def __init__(self, database):
        self.database = database

    def get_connection(self):
        if self.con is not None:
            return self.con
        self.con = self.create_connection()
        return self.con

    def create_connection(self):
        try:
            conn = sqlite3.connect(self.database, check_same_thread=False)
            return conn
        except ImportError as e:
            print(e)
        return None
