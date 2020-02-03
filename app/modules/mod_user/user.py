from app.modules.mod_insert.insert import Insert
from app.modules.mod_export.export import Export

class User:
    def __init__(self, user_id):
        self.user_id = user_id
        self.obj1 = Insert(user_id)
        self.obj2 = Export(user_id)

    
    def get_id(self):
        return self.user_id