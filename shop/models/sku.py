from decimal import Decimal
from shop.models.spu import Spu

class Sku:
    def __init__(self, sku_id, spu_id, name, spec_values, price:Decimal, sale_price:Decimal, stock:Decimal, expiry):
        self.sku_id = sku_id
        self.spu_id = spu_id
        self.name = name
        self.spec_values = spec_values
        self.price = price
        self.sale_price = sale_price
        self.stock = stock
        self.expiry = expiry

    def __repr__(self):
        return f"<Sku {self.sku_id}, {self.name})>"

    def __str__(self):
        return {self.name}