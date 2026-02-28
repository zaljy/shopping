import sqlite3
from decimal import Decimal
from shop.models.sku import Sku
from shop.repository.sku_repository import SkuRepository

class SkuService:
    def __init__(self, repo:SkuRepository):
        self.repo = repo

    def create_sku(self, sku_id, spu_id, name, spec_values, price:Decimal, sale_price:Decimal, stock:Decimal, expiry):
        if stock <= 0:
            raise ValueError('数量应为正数')
        sku = Sku(sku_id, spu_id, name, spec_values, price, sale_price, stock, expiry)
        try:
            self.repo.save_sku(sku)
        except sqlite3.IntegrityError as e:
            raise ValueError(F"库存记录{sku_id} 已存在") from e
        except Exception as e:
            raise RuntimeError(F"创建库存失败 {e}") from e

    #需要修改
    def update_sku_stock(self, sku_id, new_stock:Decimal):
        sku = self.get_sku_by_id(sku_id)
        if not sku:
            #后续需要修改函数，如果不存在则需要在数据库表中新增
            return None
        else:
            self.repo.update_sku_stock(sku_id, new_stock)
            return None

    def get_sku_by_id(self, sku_id):
        return self.repo.get_sku_by_id(sku_id)

    def get_all_sku(self):
        return self.repo.get_all_sku()