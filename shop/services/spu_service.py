from shop.repository.spu_repository import SpuRepository
from shop.models.spu import Spu

class SpuService:
    def __init__(self, repo: SpuRepository):
        self.repo = repo

    def create_spu(self, spu_id, name, brand, category_id, description, image_urls, status, created_time, updated_time):
        spu = Spu(spu_id, name, brand, category_id, description, image_urls, status, created_time, updated_time)
        self.repo.save_spu(spu)
        return spu

    def delete_spu(self, spu_id):
        if not self.repo.get_spu_by_id(spu_id):
            raise ValueError(f"商品ID{spu_id}不存在")
        self.repo.delete_spu(spu_id)

    def get_spu_by_id(self, spu_id):
        if not self.repo.get_spu_by_id(spu_id):
            raise ValueError(f"商品ID{spu_id}不存在")
        return self.repo.get_spu_by_id(spu_id)

    def get_all_spu(self):
        return self.repo.get_all_spu()