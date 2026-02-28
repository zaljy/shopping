from shop.models.spu import Spu
from shop.repository.spu_repository import
from decimal import Decimal

class CartItem:
    def __init__(self, product:Spu, quantity:Decimal):
        self.product = product
        self.quantity = quantity
    @property
    def sub_total(self):
        return self.product.price * self.quantity

class Cart:
    def __init__(self):
        self.cart_items = []

    def add_item(self, cart_item:CartItem):
        if cart_item.product.
        self.cart_items.append(cart_item)
