from utils.base_dal import BaseDal
from .models import User

class UserDal(BaseDal):

    def __init__(self):
        super().__init__(model=User)        


user_dal = UserDal()
