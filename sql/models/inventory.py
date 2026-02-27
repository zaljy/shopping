from decimal import Decimal
from sql.models.product import Product

class Inventory:
    #管理商品库存
    def __init__(self, product:Product, quantity:Decimal):
        self.product = product
        self.quantity = quantity