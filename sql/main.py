from sql.database import Database
from sql.repository.user_repository import UserRepository
from sql.repository.product_repository import ProductRepository
from sql.services.product_service import ProductService
from sql.repository.inventory_repository import InventoryRepository
from sql.services.inventory_service import InventoryService
from decimal import Decimal
from sql.repository.user_repository import UserRepository
from sql.services.user_service import UserService

def main():
    db = Database('test.db')
    inventory_repo = InventoryRepository(db)
    inventory_service = InventoryService(inventory_repo)
    product_repo = ProductRepository(db)
    product_service = ProductService(product_repo)
    user_repository = UserRepository(db)
    user_service = UserService(user_repository)
    # product_service.create_product(1002,"香蕉","水果",4,"好吃不贵的香蕉","kg",6,180)
    # product = product_service.get_product_by_id(1002)
    # # # inventory_repo.create_table()
    # inventory_service.create_inventory(product.product_id,300)
    # inventory_service.update_inventory_quantity(product.product_id,50)
    try:
        user_service.create_user(1001,"janana","admin1234",1231001200)
    except ValueError as e:
        print(e)



if __name__ == '__main__':
    main()