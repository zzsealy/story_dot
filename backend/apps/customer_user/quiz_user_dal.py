from utils.base_dal import BaseDal
from .models import CustomerUser

class QuizUserDal(BaseDal):

    def __init__(self):
        super().__init__(model=CustomerUser)        


quiz_user_dal = QuizUserDal()
