from utils.base_dal import BaseDal
from .models import QuizUser

class QuizUserDal(BaseDal):

    def __init__(self):
        super().__init__(model=QuizUser)        


quiz_user_dal = QuizUserDal()
