class Product:
    def __init__(self,product_id,name,category_id,price,description,unit,sale_price,shelf_life):
        self.product_id = product_id
        self.name = name
        self.category_id = category_id
        self.price = price
        self.description = description
        self.unit = unit
        self.sale_price = sale_price
        self.shelf_life = shelf_life

    def __repr__(self):
        return  f"Product(product_id: {self.product_id} name: {self.name} description: {self.description})"