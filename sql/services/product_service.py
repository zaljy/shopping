from sql.repository.product_repository import ProductRepository
from sql.models.product import Product

class ProductService:
    def __init__(self,repo: ProductRepository):
        self.repo = repo

    def create_product(self,product_id,name,category_id,price,description,unit,sale_price,shelf_life):
        if price < 0 or sale_price < 0:
            raise ValueError("价格和售价不能小于0")
        if shelf_life <= 0:
            raise ValueError("保质期必须为正数")
        if not name or not name.strip():
            raise ValueError("商品名称不能为空")
        if self.repo.get_product_by_id(product_id):
            raise ValueError(f"商品ID{product_id}已存在")
        product = Product(
            product_id=product_id,
            name=name,
            category_id=category_id,
            price=price,
            description=description,
            unit=unit,
            sale_price=sale_price,
            shelf_life=shelf_life
        )
        self.repo.save_product(product)#把商品保存到数据库
        return product

    def update_price(self,product_id,new_price):
        if new_price < 0:
            raise ValueError("价格不能小于0")
        product = self.repo.get_product_by_id(product_id)
        if not product:
            raise ValueError(f"商品ID{product_id}不存在")
        old_price = product.price
        self.repo.update_product(product_id,price=new_price)
        print(f"商品ID{product_id}价格已从{old_price}修改为{new_price}")
        return self.repo.get_product_by_id(product_id)

    def delete_product(self,product_id):
        if not self.repo.get_product_by_id(product_id):
            raise ValueError(f"商品ID{product_id}不存在")
        self.repo.delete_product(product_id)

    def get_product_by_id(self,product_id):
        if not self.repo.get_product_by_id(product_id):
            raise ValueError(f"商品ID{product_id}不存在")
        return self.repo.get_product_by_id(product_id)

    def get_all_products(self):
        return self.repo.get_all_products()