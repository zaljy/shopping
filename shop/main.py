from datetime import datetime
from shop.database import Database
from shop.repository.user_repository import UserRepository
from shop.repository.spu_repository import SpuRepository
from shop.services.spu_service import SpuService
from shop.repository.sku_repository import SkuRepository
from shop.services.sku_service import SkuService
from decimal import Decimal
from shop.repository.user_repository import UserRepository
from shop.services.user_service import UserService
from shop.models.category import Category
from shop.repository.category_repository import CategoryRepository

def main():
    db = Database('test.db')
    spu_repo = SpuRepository(db)
    spu_service = SpuService(spu_repo)
    sku_repo = SkuRepository(db)
    sku_service = SkuService(sku_repo)
    category_repo = CategoryRepository(db)
    # category_repo.create_table()
    # spu_repo.create_table()
    # sku_repo.create_table()
    spu_service.create_spu(1000100,"苹果手机","apple",1,"苹果手机，值得信赖",
                           '',1,datetime.now(),datetime.now())
    sku_service.create_sku(1001,1000100,"苹果14","颜色:土豪金,内存:512G",6400,5800,100,180)




if __name__ == '__main__':
    main()