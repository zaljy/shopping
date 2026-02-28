from shop.database import Database
from shop.models.user import User

class UserRepository:
    def __init__(self,db:Database):
        self.db = db

    def create_table(self):
        sql = """
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY UNIQUE NOT NULL,
            username TEXT NOT NULL,
            password VARCHAR NOT NULL,
            phone_number TEXT UNIQUE
        )
        """
        return self.db.execute(sql)

    def save_user(self, user:User):
        sql = "INSERT INTO users (user_id,username,password,phone_number) VALUES (?,?,?,?)"
        params = (user.user_id,user.username,user.password,user.phone_number)
        return self.db.execute(sql,params)

    def delete_user(self,user_id):
        sql = 'DELETE FROM users WHERE user_id = ?'
        return self.db.execute(sql,(user_id,))

    def get_user_by_id(self, user_id):
        sql = 'SELECT * FROM users WHERE user_id = ?'
        row = self.db.fetchone(sql,(user_id,))
        return self._row_to_user(row)

    def get_all_users(self):
        sql = 'SELECT * FROM users'
        rows = self.db.fetchall(sql)
        return [self._row_to_user(row) for row in rows]

    def update_user(self, user_id, **kwargs):
        if not kwargs:
            return None
        else:
            set_clause = ','.join(f'{k} = ?' for k in kwargs)
            values = list(kwargs.values()) + [user_id]
            sql = f'UPDATE users SET {set_clause} WHERE user_id = ?'
            return self.db.execute(sql,values)

    @staticmethod
    def _row_to_user(row):
        if not row:
            return None
        else:
            # 把数据库返回行转成Product对象
            return User(
                user_id = row["user_id"],
                username = row["username"],
                password= row["password"],
                phone_number = row["phone_number"]
            )