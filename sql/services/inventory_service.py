from decimal import Decimal
from sql.models.inventory import Inventory
from sql.models.product import Product
from sql.repository.inventory_repository import InventoryRepository

class InventoryService:
    def __init__(self,repo:InventoryRepository):
        self.repo = repo
        self.inventory = []

    def create_inventory(self,product:Product,quantity:Decimal):
        if quantity <= 0:
            raise ValueError('数量应为正数')
        inventory = Inventory(product,quantity)
        self.repo.save_inventory(inventory)

    def update_inventory_quantity(self,product,new_quantity:Decimal):
        if not self.repo.get_inventory_by_id(product.product_id):
            self.create_inventory(product,new_quantity)
        else:
            quantity = self.repo.get_inventory_by_id(product.product_id)[2] + new_quantity
            inventory = Inventory(product,quantity)
            self.repo.delete_inventory(product.product_id)
            self.repo.save_inventory(inventory)



