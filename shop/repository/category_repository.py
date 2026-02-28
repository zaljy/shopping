from shop.database import Database
from shop.models.category import Category

class CategoryRepository:
    def __init__(self,db:Database):
        self.db = db

    def create_table(self):
        sql = """
        CREATE TABLE category (
            category_id INTEGER PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            parent_id INT DEFAULT NULL,
            level INT DEFAULT NULL,
            sort_order INT DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (parent_id) REFERENCES category(category_id) ON DELETE CASCADE
            )
        """
        return self.db.execute(sql)