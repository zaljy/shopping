from sql.database import Database
from sql.repository.user_repository import UserRepository
from sql.repository.product_repository import ProductRepository
from sql.services.product_service import ProductService


def main():
    db = Database('test.db')
    user_manager = UserRepository(db)
    # product_repo = ProductRepository(db)


    # user1 = User(1003,'wzw',1234,15072352627)
    # user_manager.add_user(user1)
    # user_manager.create_user(1004,'hmt',1234,15500000000)
    # product_manager.create_product(1001,"苹果","水果",4,"营养价值高","kg",8,15)

if __name__ == '__main__':
    main()