import sqlite3


class DBHelper:
    def __init__(self, dbname='todo.sqlite'):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    def setup(self):
        stmt = "CREATE TABLE IF NOT EXISTS items (description text)"
        self.conn.execute(stmt)
        self.conn.commit()

    def add_item(self, description):
        stmt = "INSERT INTO items (description) VALUES (?)"
        args = (description,)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def delete_item(self, description):
        stmt = "DELETE FROM items WHERE description = (?)"
        args = (description,)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def get_items(self):
        stmt = "SELECT description FROM items"
        return [x[0] for x in self.conn.execute(stmt)]
