from ninja import Router
from apps.quiz_user.apis.email_view import router as email_router
# from apps.user.apis.captcha_view import router as captcha_router
from apps.quiz_user.apis.user_operation_view import router as user_operation_router

user_router = Router()
user_router.add_router('/', user_operation_router) # 只是发送验证码
# user_router.add_router('/', captcha_router)
user_router.add_router('/', email_router) # 校验验证码成功之后才注册用户