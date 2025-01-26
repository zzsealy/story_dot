from ninja import Router
from apps.user.apis.user_operation import router as user_operation_router

user_router = Router()
user_router.add_router('/', user_operation_router)