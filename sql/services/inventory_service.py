from decimal import Decimal
from sql.models.inventory import Inventory
from sql.repository.inventory_repository import InventoryRepository

class InventoryService:
    def __init__(self,repo:InventoryRepository):
        self.repo = repo
        self.inventory = []

    def create_inventory(self,product_id,quantity:Decimal):
        if quantity <= 0:
            raise ValueError('数量应为正数')
        inventory = Inventory(product_id,quantity)
        self.repo.save_inventory(inventory)

    def update_inventory_quantity(self,product_id,new_quantity:Decimal):
        if not self.repo.get_inventory_by_id(product_id):
            self.create_inventory(product_id,new_quantity)
        else:
            update_quantity = self.repo.get_inventory_by_id(product_id).quantity + new_quantity
            self.repo.update_inventory(product_id,quantity = update_quantity)

    def get_inventory_by_id(self,product_id):
        return self.repo.get_inventory_by_id(product_id)

    def get_all_inventory(self):
        return self.repo.get_all_inventory()