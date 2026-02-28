class Category:
    def __init__(self,category_id,name,parent_id,level,sort_order,created_at,updated_at):
        self.category_id = category_id
        self.name = name
        self.parent_id = parent_id
        self.level = level
        self.sort_order = sort_order
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return f"<Category {self.category_id}: {self.name}>"

    def __str__(self):
        return self.name