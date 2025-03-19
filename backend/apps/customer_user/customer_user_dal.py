from utils.base_dal import BaseDal
from .models import CustomerUser

class CustomerUserDal(BaseDal):

    def __init__(self):
        super().__init__(model=CustomerUser)        


customer_user_dal = CustomerUserDal()
