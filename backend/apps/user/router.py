from ninja import Router
from apps.user.apis.user_operation_view import router as user_operation_router
from apps.user.apis.captcha_view import router as captcha_router

user_router = Router()
user_router.add_router('/', user_operation_router)
user_router.add_router('/', captcha_router)