from sql.database import Database
from sql.models.product import Product

class ProductRepository:
    def __init__(self,db:Database):
        self.db = db

    def create_table(self):
        sql = """
        CREATE TABLE products (
            product_id INT PRIMARY KEY NOT NULL,
            name VARCHAR(255) NOT NULL,
            category_id INT,
            price DECIMAL(10,2) NOT NULL,
            description TEXT,
            unit VARCHAR(50),
            sale_price DECIMAL(10,2) NOT NULL,
            shelf_life INT NOT NULL
        )
        """
        return self.db.execute(sql)

    def save_product(self, product:Product):
        sql = """
        INSERT INTO products 
            (product_id,name,category_id,price,description,unit,sale_price,shelf_life) 
            VALUES (?,?,?,?,?,?,?,?)
        """
        params = (product.product_id,product.name,product.category_id,product.price,product.description,
                  product.unit,product.sale_price,product.shelf_life)
        return self.db.execute(sql,params)

    def delete_product(self,product_id):
        sql = 'DELETE FROM products WHERE product_id = ?'
        return self.db.execute(sql,(product_id,))

    def update_product(self, product_id, **kwargs):
        if not kwargs:
            return None
        else:
            set_clause = ','.join(f'{k} = ?' for k in kwargs)
            values = list(kwargs.values()) + [product_id]
            sql = f'UPDATE products SET {set_clause} WHERE product_id = ?'
            return self.db.execute(sql,values)

    def get_product_by_id(self, product_id):
        sql = 'SELECT * FROM products WHERE product_id = ?'
        row = self.db.fetchone(sql, (product_id,))
        if row:
            return self._row_to_product(row)
        else:
            return None

    def get_all_products(self):
        sql = 'SELECT * FROM products'
        rows = self.db.fetchall(sql)
        return [self._row_to_product(row) for row in rows]

    @staticmethod
    def _row_to_product(row):
        #把数据库返回行转成Product对象
        if not row:
            return None
        else:
            return Product(
                product_id = row['product_id'],
                name = row['name'],
                category_id = row['category_id'],
                price = row['price'],
                description = row['description'],
                unit = row['unit'],
                sale_price = row['sale_price'],
                shelf_life = row['shelf_life']
            )