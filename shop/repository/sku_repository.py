from decimal import Decimal
from shop.database import Database
from shop.models.sku import Sku

class SkuRepository:
    def __init__(self,db:Database):
        self.db = db

    def create_table(self):
        sql = """
        CREATE TABLE sku (
            sku_id INTEGER PRIMARY KEY,
            spu_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            spec_values TEXT, 
            price NUMERIC NOT NULL,
            sale_price NUMERIC NOT NULL,
            stock NUMERIC NOT NULL DEFAULT 0.00,
            expiry TEXT,
            FOREIGN KEY (spu_id) REFERENCES spu(spu_id) ON DELETE CASCADE
            )
        """
        return self.db.execute(sql)

    def save_sku(self, sku:Sku):
        sql = """
        INSERT INTO sku 
            (sku_id,spu_id,name,spec_values,price,sale_price,stock,expiry) 
            VALUES (?,?,?,?,?,?,?,?)
        """
        params = (sku.sku_id, sku.spu_id, sku.name, sku.spec_values, sku.price, sku.sale_price, sku.stock, sku.expiry)
        return self.db.execute(sql,params)

    def delete_sku(self, sku_id):
        sql = 'DELETE FROM sku WHERE sku_id = ?'
        return self.db.execute(sql, (sku_id,))

    def update_sku_stock(self, sku_id, new_stock):
        sql = 'UPDATE sku SET stock = stock +? WHERE sku_id = ?'
        return self.db.execute(sql, (new_stock, sku_id))

    def update_sku(self, sku_id, **kwargs):
        if not kwargs:
            return None
        else:
            set_clause = ','.join(f'{k} = ?' for k in kwargs)
            values = list(kwargs.values()) + [sku_id]
            sql = f'UPDATE sku SET {set_clause} WHERE slu_id = ?'
            return self.db.execute(sql,values)

    def get_sku_by_id(self, sku_id):
        sql = 'SELECT * FROM sku WHERE sku_id = ?'
        row = self.db.fetchone(sql, (sku_id,))
        if row:
            return self._row_to_sku(row)
        else:
            return None

    def get_all_sku(self):
        sql = 'SELECT * FROM sku'
        rows = self.db.fetchall(sql)
        return [self._row_to_sku(row) for row in rows]

    @staticmethod
    def _row_to_sku(row):
        if not row:
            return None
        else:
            sku = Sku(row['sku_id'], row['spu_id'], row['name'], row['spec_values'],
                      row['price'], row['sale_price'], row['stock'], row['expiry'])
        return sku