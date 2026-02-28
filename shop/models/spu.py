class Spu:
    def __init__(self, spu_id, name, brand, category_id, description, image_urls, status, created_time, updated_time):
        self.spu_id = spu_id
        self.name = name
        self.brand = brand
        self.category_id = category_id
        self.description = description
        self.image_urls = image_urls
        self.status = status
        self.created_time = created_time
        self.updated_time = updated_time

    def __repr__(self):
        return  f"<Product {self.spu_id} : {self.name}>"

    def __str__(self):
        return self.name