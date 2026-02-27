# models.py
import sqlite3
import hashlib

DB_PATH = 'supermarket.db'


def get_db():
    return sqlite3.connect(DB_PATH)


def init_db():
    """初始化数据库表结构，并创建默认管理员"""
    conn = get_db()
    c = conn.cursor()

    # 商品表（增加 barcode 字段）
    c.execute('''CREATE TABLE IF NOT EXISTS products
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  barcode TEXT UNIQUE,          -- 条码，可选
                  name TEXT NOT NULL,
                  category TEXT,
                  price REAL NOT NULL,
                  cost REAL NOT NULL,
                  supplier TEXT)''')

    # 库存表
    c.execute('''CREATE TABLE IF NOT EXISTS inventory
                 (product_id INTEGER PRIMARY KEY,
                  quantity INTEGER NOT NULL DEFAULT 0,
                  min_threshold INTEGER DEFAULT 5,
                  FOREIGN KEY(product_id) REFERENCES products(id))''')

    # 进货记录
    c.execute('''CREATE TABLE IF NOT EXISTS purchases
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  product_id INTEGER NOT NULL,
                  quantity INTEGER NOT NULL,
                  cost REAL NOT NULL,
                  purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  FOREIGN KEY(product_id) REFERENCES products(id))''')

    # 销售记录
    c.execute('''CREATE TABLE IF NOT EXISTS sales
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  product_id INTEGER NOT NULL,
                  quantity INTEGER NOT NULL,
                  price REAL NOT NULL,
                  sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  FOREIGN KEY(product_id) REFERENCES products(id))''')

    # 员工表
    c.execute('''CREATE TABLE IF NOT EXISTS employees
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE NOT NULL,
                  password TEXT NOT NULL)''')

    # 插入默认管理员（admin/admin123）
    c.execute("SELECT * FROM employees WHERE username='admin'")
    if not c.fetchone():
        hashed = hashlib.sha256("admin123".encode()).hexdigest()
        c.execute("INSERT INTO employees (username, password) VALUES (?, ?)", ("admin", hashed))

    conn.commit()
    conn.close()


# 常用数据库操作
def query(sql, params=(), one=False):
    conn = get_db()
    cur = conn.execute(sql, params)
    rv = cur.fetchall()
    cur.close()
    conn.close()
    return (rv[0] if rv else None) if one else rv


def execute(sql, params=()):
    conn = get_db()
    cur = conn.execute(sql, params)
    conn.commit()
    last_id = cur.lastrowid
    cur.close()
    conn.close()
    return last_id