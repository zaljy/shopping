from sql.database import Database
from sql.repository.user_repository import UserRepository
from sql.repository.product_repository import ProductRepository
from sql.services.product_service import ProductService
from sql.repository.inventory_repository import InventoryRepository
from sql.services.inventory_service import InventoryService
from decimal import Decimal

def main():
    db = Database('test.db')
    inventory_repo = InventoryRepository(db)
    inventory_service = InventoryService(inventory_repo)
    product_repo = ProductRepository(db)
    product_service = ProductService(product_repo)

    product = product_service.get_product_by_id(1001)
    # inventory_repo.create_table()
    # inventory_service.create_inventory(product,100)
    inventory_service.update_inventory_quantity(product,50)


if __name__ == '__main__':
    main()