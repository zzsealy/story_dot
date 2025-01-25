from ninja import Router
from apps.user.apis.user_status import router as user_status_router

user_router = Router()
user_router.add_router('/', user_status_router)