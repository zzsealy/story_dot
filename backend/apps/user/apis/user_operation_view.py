from ninja import Router, Schema, ModelSchema, Field

from .captcha_view import get_register_ver_code_pass_cache_key
from utils.cache import cache

router = Router()

"""
注册
"""
class RegisterOut(Schema):
    status_code: int
    message: str
    user_id: int

class RegisterSchema(Schema):
    email: str = Field(description='邮箱')
    nick_name: str = Field(description='昵称')
    password: str = Field(description='密码')
    password_repeat: str = Field(description='重复密码')

@router.post('/register', response=RegisterOut)
def register(request, payload: RegisterSchema):
    ip = request.META.get('REMOTE_ADDR')
    is_valid_ver_code = cache.get(get_register_ver_code_pass_cache_key(ip))
    if is_valid_ver_code:
        cache.delete(get_register_ver_code_pass_cache_key(ip))
        return {'status_code': 200, 'message': '注册成功', 'user_id': 1}
    else:
        return {'status_code': 400, 'message': '请进行人际验证', 'user_id': 1}


"""
登录 
"""
class LoginSchema(Schema):
    username: str = Field(None, alias='username')
    password: str = Field(None, alias='password')

class Out(Schema):
    token: str

@router.post('/login', response=Out, auth=None)
def login(request, data: LoginSchema):
    return {'status': 'ok', 'token': '123132'}





