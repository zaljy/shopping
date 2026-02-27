import sqlite3
from contextlib import contextmanager

class Database:
    def __init__(self, db_file):
        self.db_file = db_file

    @contextmanager
    def get_db(self):
        conn = sqlite3.connect(self.db_file)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except sqlite3.Error as e:
            print(f"数据库错误：{e}")
            conn.rollback()
        finally:
            conn.close()

    def execute(self,sql,params = None):
        with self.get_db() as conn:
            c = conn.cursor()
            c.execute(sql,params or ())
            return c.rowcount

    def fetchall(self,sql,params = None):
        with self.get_db() as conn:
            c = conn.cursor()
            c.execute(sql,params or ())
            return c.fetchall()

    def fetchone(self,sql,params = None):
        with self.get_db() as conn:
            c = conn.cursor()
            c.execute(sql,params or ())
            return c.fetchone()
