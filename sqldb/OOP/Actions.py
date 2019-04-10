from Database import Database


class Actions:
    database = None

    def __init__(self, database):
        self.database = database

    def create_table(self, create_table_sql):
        try:
            c = self.database.get_connection()
            c.execute(create_table_sql)
        except ImportError as e:
            print(e)

    def create_tables(self):
        sql_create_favids_table = """ CREATE TABLE IF NOT EXISTS favids (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        fav1 text ,
                                        fav2 text ,
                                        fav3 text ,
                                        fav4 text
                                        ); """

        self.create_table(sql_create_favids_table)

    def del_fav(self, usr, fav):
        con = self.database.get_connection()
        query = '''UPDATE favids SET %s = null where id = %s''' % (fav, usr)
        print query
        cur = con.cursor()
        cur.execute(query)
        con.commit()

    def add_fav(self, usr, fav, busid):
        con = self.database.get_connection()
        query = '''UPDATE favids SET %s = '%s' where id = %s''' % (
            fav, busid, usr)
        print query
        cur = con.cursor()
        cur.execute(query)
        con.commit()

    def add_favs(self, usr, fav1, fav2, fav3, fav4):
        con = self.database.get_connection()
        cur = con.cursor()
        cur.execute("INSERT INTO favids (name,fav1,fav2,fav3,fav4) VALUES (?,?,?,?,?)",
                    (usr, fav1, fav2, fav3, fav4))
        con.commit()

    def select_all(self, sql):
        con = self.database.get_connection()
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("select * from favids")
        rows_fav = cur.fetchall()
        return rows_fav

    def select_usr(self, sql, usr):
        con = self.database.get_connection()
        con.row_factory = sql.Row
        cur = con.cursor()
        query = '''SELECT * FROM favids WHERE id = %s ''' % (usr)
        cur.execute(query)
        rows_fav = cur.fetchall()
        return self.dict_factory(cur, rows_fav[0])

    def dict_factory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d
