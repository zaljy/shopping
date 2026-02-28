from shop.database import Database
from shop.models.spu import Spu

class SpuRepository:
    def __init__(self,db:Database):
        self.db = db

    def create_table(self):
        sql = """
        CREATE TABLE spu (
            spu_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            brand TEXT,
            category_id INTEGER,
            description TEXT,
            image_urls TEXT,
            status INTEGER DEFAULT 1,
            created_time TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_time TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (category_id) REFERENCES category(category_id) ON DELETE SET NULL
            )
        """
        return self.db.execute(sql)

    def save_spu(self, spu:Spu):
        sql = """
        INSERT INTO spu (
            spu_id, name, brand, category_id, description, image_urls, status,
            created_time, updated_time
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (spu.spu_id, spu.name, spu.brand, spu.category_id, spu.description,
                  spu.image_urls, spu.status, spu.created_time, spu.updated_time)
        return self.db.execute(sql,params)

    def delete_spu(self, spu_id):
        sql = 'DELETE FROM spu WHERE sku_id = ?'
        return self.db.execute(sql, (spu_id,))

    def update_spu(self, spu_id, **kwargs):
        if not kwargs:
            return None
        else:
            set_clause = ','.join(f'{k} = ?' for k in kwargs)
            values = list(kwargs.values()) + [spu_id]
            sql = f'UPDATE spu SET {set_clause} WHERE spu_id = ?'
            return self.db.execute(sql,values)

    def get_spu_by_id(self, spu_id):
        sql = 'SELECT * FROM spu WHERE spu_id = ?'
        row = self.db.fetchone(sql, (spu_id,))
        if row:
            return self._row_to_spu(row)
        else:
            return None

    def get_all_spu(self):
        sql = 'SELECT * FROM spu'
        rows = self.db.fetchall(sql)
        return [self._row_to_spu(row) for row in rows]

    @staticmethod
    def _row_to_spu(row):
        #把数据库返回行转成Spu对象
        if not row:
            return None
        else:
            return Spu(row['spu_id'], row['name'], row['brand'], row['category_id'], row['description'],
                       row['image_urls'], row['status'], row['created_time'], row['updated_time'])