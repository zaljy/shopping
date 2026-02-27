# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from functools import wraps
import hashlib
from models import init_db, query, execute

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-in-production'  # 生产环境请修改

# 初始化数据库（首次运行自动创建表）
init_db()

# 登录装饰器
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ---------- 路由：登录/注销 ----------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = hashlib.sha256(request.form['password'].encode()).hexdigest()
        user = query("SELECT * FROM employees WHERE username=? AND password=?", (username, password), one=True)
        if user:
            session['user_id'] = user[0]
            session['username'] = user[1]
            return redirect(url_for('index'))
        else:
            flash('用户名或密码错误')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ---------- 主页 ----------
@app.route('/')
@login_required
def index():
    return render_template('index.html')

# ---------- 商品管理 ----------
@app.route('/products')
@login_required
def products():
    # 获取所有商品（含库存）
    rows = query('''SELECT p.id, p.barcode, p.name, p.category, p.price, p.cost, p.supplier,
                           i.quantity, i.min_threshold
                    FROM products p
                    LEFT JOIN inventory i ON p.id = i.product_id
                    ORDER BY p.id''')
    return render_template('products.html', products=rows)

@app.route('/product/add', methods=['POST'])
@login_required
def add_product():
    barcode = request.form.get('barcode') or None
    name = request.form['name']
    category = request.form['category']
    price = float(request.form['price'])
    cost = float(request.form['cost'])
    supplier = request.form['supplier']
    try:
        product_id = execute('''INSERT INTO products (barcode, name, category, price, cost, supplier)
                                VALUES (?,?,?,?,?,?)''', (barcode, name, category, price, cost, supplier))
        execute("INSERT INTO inventory (product_id, quantity, min_threshold) VALUES (?, 0, 5)", (product_id,))
        flash('商品添加成功')
    except Exception as e:
        flash(f'添加失败：{str(e)}')
    return redirect(url_for('products'))

@app.route('/product/update/<int:product_id>', methods=['POST'])
@login_required
def update_product(product_id):
    barcode = request.form.get('barcode') or None
    name = request.form['name']
    category = request.form['category']
    price = float(request.form['price'])
    cost = float(request.form['cost'])
    supplier = request.form['supplier']
    execute('''UPDATE products SET barcode=?, name=?, category=?, price=?, cost=?, supplier=?
               WHERE id=?''', (barcode, name, category, price, cost, supplier, product_id))
    flash('商品信息已更新')
    return redirect(url_for('products'))

@app.route('/product/delete/<int:product_id>')
@login_required
def delete_product(product_id):
    execute("DELETE FROM inventory WHERE product_id=?", (product_id,))
    execute("DELETE FROM products WHERE id=?", (product_id,))
    flash('商品已删除')
    return redirect(url_for('products'))

# ---------- 库存管理 ----------
@app.route('/inventory')
@login_required
def inventory():
    rows = query('''SELECT p.id, p.name, i.quantity, i.min_threshold
                    FROM products p
                    JOIN inventory i ON p.id = i.product_id
                    ORDER BY i.quantity < i.min_threshold DESC, p.id''')
    return render_template('inventory.html', inventory=rows)

@app.route('/inventory/adjust', methods=['POST'])
@login_required
def adjust_inventory():
    product_id = int(request.form['product_id'])
    delta = int(request.form['delta'])
    execute("UPDATE inventory SET quantity = quantity + ? WHERE product_id=?", (delta, product_id))
    flash('库存调整成功')
    return redirect(url_for('inventory'))

# ---------- 进货管理 ----------
@app.route('/purchases')
@login_required
def purchases():
    # 显示进货记录
    rows = query('''SELECT pu.id, p.name, pu.quantity, pu.cost, pu.purchase_date
                    FROM purchases pu
                    JOIN products p ON pu.product_id = p.id
                    ORDER BY pu.purchase_date DESC''')
    return render_template('purchase.html', purchases=rows)

@app.route('/purchase/add', methods=['POST'])
@login_required
def add_purchase():
    product_id = int(request.form['product_id'])
    quantity = int(request.form['quantity'])
    cost = float(request.form['cost'])
    # 验证商品存在
    product = query("SELECT id FROM products WHERE id=?", (product_id,), one=True)
    if not product:
        flash('商品不存在')
        return redirect(url_for('purchases'))
    execute("INSERT INTO purchases (product_id, quantity, cost) VALUES (?,?,?)", (product_id, quantity, cost))
    execute("UPDATE inventory SET quantity = quantity + ? WHERE product_id=?", (quantity, product_id))
    flash('进货录入成功')
    return redirect(url_for('purchases'))

# ---------- 销售管理（含API）----------
@app.route('/sales')
@login_required
def sales():
    # 显示销售记录
    rows = query('''SELECT s.id, p.name, s.quantity, s.price, s.sale_date
                    FROM sales s
                    JOIN products p ON s.product_id = p.id
                    ORDER BY s.sale_date DESC''')
    return render_template('sale.html', sales=rows)

@app.route('/api/product/<barcode>')
@login_required
def api_product_by_barcode(barcode):
    """根据条码或ID查询商品（用于收银台AJAX）"""
    # 先按条码查，再按ID查
    product = query("SELECT id, name, price FROM products WHERE barcode=?", (barcode,), one=True)
    if not product:
        # 尝试按ID查（兼容旧数据）
        product = query("SELECT id, name, price FROM products WHERE id=?", (barcode,), one=True)
    if product:
        return jsonify({'id': product[0], 'name': product[1], 'price': product[2]})
    else:
        return jsonify({'error': '商品不存在'}), 404

@app.route('/api/sale/checkout', methods=['POST'])
@login_required
def api_checkout():
    """结算购物车"""
    data = request.get_json()
    items = data.get('items', [])
    if not items:
        return jsonify({'error': '购物车为空'}), 400

    conn = models.get_db()  # 注意：这里需要导入 models 中的 get_db
    c = conn.cursor()
    try:
        sale_ids = []
        for item in items:
            product_id = item['id']
            quantity = item['quantity']
            price = item['price']
            # 检查库存
            stock = c.execute("SELECT quantity FROM inventory WHERE product_id=?", (product_id,)).fetchone()
            if not stock or stock[0] < quantity:
                raise Exception(f"商品 {product_id} 库存不足")
            # 插入销售记录
            c.execute("INSERT INTO sales (product_id, quantity, price) VALUES (?,?,?)",
                      (product_id, quantity, price))
            sale_ids.append(c.lastrowid)
            # 扣减库存
            c.execute("UPDATE inventory SET quantity = quantity - ? WHERE product_id=?",
                      (quantity, product_id))
        conn.commit()
        # 返回最后一个销售记录的ID作为小票ID（简单处理，实际可用销售单号）
        return jsonify({'success': True, 'sale_id': sale_ids[-1] if sale_ids else None})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

# ---------- 小票打印 ----------
@app.route('/receipt/<int:sale_id>')
@login_required
def receipt(sale_id):
    # 查询销售主记录（这里我们取该销售ID对应的商品明细，但实际一次销售可能有多条记录）
    # 简单实现：假设 sale_id 是 sales 表中的 id，且一次销售对应多条记录（同一次结算）
    # 我们可以通过查询同一时间附近的记录来关联，但这里简化：直接查该ID的单条记录
    sale = query("SELECT s.id, s.product_id, s.quantity, s.price, s.sale_date, p.name "
                 "FROM sales s JOIN products p ON s.product_id = p.id WHERE s.id=?", (sale_id,), one=True)
    if not sale:
        flash('小票不存在')
        return redirect(url_for('sales'))
    # 为了显示多条，我们可以按时间分组，但简单起见，这里只显示一条。
    # 更合理的方式：前端传入一个购物车快照，或者使用销售单号。
    # 这里我们采用折中：显示该条记录，并计算总额
    total = sale[2] * sale[3]
    items = [{
        'name': sale[5],
        'price': sale[3],
        'quantity': sale[2],
        'subtotal': total
    }]
    return render_template('receipt.html', sale={
        'id': sale[0],
        'date': sale[4]
    }, items=items, total=total)

# ---------- 报表统计 ----------
@app.route('/reports')
@login_required
def reports():
    # 销售统计（按商品）
    sales_stats = query('''SELECT p.id, p.name, SUM(s.quantity), SUM(s.quantity * s.price)
                           FROM sales s
                           JOIN products p ON s.product_id = p.id
                           GROUP BY p.id''')
    # 进货统计
    purchase_stats = query('''SELECT p.id, p.name, SUM(pu.quantity), SUM(pu.quantity * pu.cost)
                              FROM purchases pu
                              JOIN products p ON pu.product_id = p.id
                              GROUP BY p.id''')
    # 库存价值
    inventory_value = query('''SELECT p.id, p.name, i.quantity, p.cost, i.quantity * p.cost AS total_cost,
                                      p.price, i.quantity * p.price AS total_price
                               FROM products p
                               JOIN inventory i ON p.id = i.product_id''')
    total_cost_value = sum(row[4] for row in inventory_value) if inventory_value else 0
    total_price_value = sum(row[6] for row in inventory_value) if inventory_value else 0

    return render_template('reports.html',
                           sales_stats=sales_stats,
                           purchase_stats=purchase_stats,
                           inventory_value=inventory_value,
                           total_cost_value=total_cost_value,
                           total_price_value=total_price_value)

if __name__ == '__main__':
    app.run(debug=True)