from decimal import Decimal
from sql.models.product import Product

class Inventory:
    #管理商品库存
    def __init__(self, product_id, quantity:Decimal):
        self.product_id = product_id
        self.quantity = quantity

    def __repr__(self):
        return f"Inventory(product_id: {self.product_id}, quantity: {self.quantity})"