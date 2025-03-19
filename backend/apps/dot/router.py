
from ninja import Router
from apps.dot.apis.dot_view import router as dot_view

dot_router = Router()



dot_router.add_router('/', dot_view) # 只是发送验证码