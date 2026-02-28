from models.user import User
from sql.repository.user_repository import UserRepository
import hash_password

class UserService:
    def __init__(self,repo:UserRepository):
        self.repo = repo

    def create_user(self,user_id,name,password,phone_number):
        if not name or not password:
            raise ValueError('姓名和密码不能为空')
        #在创建数据库表的时候就把user_id设置成唯一
        # if self.repo.get_user_by_id(user_id):
        #     raise ValueError(f'用户ID{user_id}已存在')
        user = User(
            user_id=user_id,
            username=name,
            password=hash_password.hash_password(password),
            phone_number=phone_number
        )
        self.repo.save_user(user)
        return user

    def update_phone_number(self,user_id,new_phone_number):
        if not self.repo.get_user_by_id(user_id):
            raise ValueError(f'用户ID{user_id}不存在')
        old_phone_number = self.repo.get_user_by_id(user_id).phone_number
        self.repo.update_user(user_id,phone_number = new_phone_number)
        print(f"用户ID{user_id}电话号码已由{old_phone_number}修改为{new_phone_number}")
        return self.repo.get_user_by_id(user_id)