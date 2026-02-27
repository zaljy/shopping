from decimal import Decimal
from sql.database import Database
from sql.models.inventory import Inventory

class InventoryRepository:
    def __init__(self,db:Database):
        self.db = db

    def create_table(self):
        sql = """
        CREATE TABLE inventory (
            product_id INT PRIMARY KEY NOT NULL,
            quantity DECIMAL(10, 3) NOT NULL
        )
        """
        return self.db.execute(sql)

    def save_inventory(self,inventory:Inventory):
        sql = """
        INSERT INTO inventory 
            (product_id,quantity) 
            VALUES (?,?)
        """
        params = (inventory.product_id,inventory.quantity)
        return self.db.execute(sql,params)

    def delete_inventory(self,product_id):
        sql = 'DELETE FROM inventory WHERE product_id = ?'
        return self.db.execute(sql,(product_id,))

    def update_inventory(self, product_id, **kwargs):
        if not kwargs:
            return None
        else:
            set_clause = ','.join(f'{k} = ?' for k in kwargs)
            values = list(kwargs.values()) + [product_id]
            sql = f'UPDATE inventory SET {set_clause} WHERE product_id = ?'
            return self.db.execute(sql,values)

    def get_inventory_by_id(self, product_id):
        sql = 'SELECT * FROM inventory WHERE product_id = ?'
        row = self.db.fetchone(sql, (product_id,))
        if row:
            return self._row_to_inventory(row)
        else:
            return None

    def get_all_inventory(self):
        sql = 'SELECT * FROM inventory'
        rows = self.db.fetchall(sql)
        return [self._row_to_inventory(row) for row in rows]

    @staticmethod
    def _row_to_inventory(row):
        inventory = Inventory(row['product_id'],row['quantity'])
        return inventory