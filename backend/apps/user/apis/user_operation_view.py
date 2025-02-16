import random
import asyncio

from django.core import signing
from asgiref.sync import sync_to_async

from utils.cache import cache
from utils.email_utils import send_email, get_email_cache_key
from ninja import Router, Schema, ModelSchema, Field
from .captcha_view import get_register_ver_code_pass_cache_key
from apps.user.user_dal import user_dal

router = Router()

"""
注册
"""
class RegisterOut(Schema):
    status_code: int
    message: str
    email_signed: str = None

class RegisterSchema(Schema):
    email: str = Field(description='邮箱')
    nick_name: str = Field(description='昵称')
    password: str = Field(description='密码')
    password_repeat: str = Field(description='重复密码')

@sync_to_async
def save_user(user):
    user.save()

@router.post('/register', response=RegisterOut)
async def register(request, payload: RegisterSchema):
    # ip = request.META.get('REMOTE_ADDR')
    # 注释验证码 采用发送邮箱的方式
    # is_valid_ver_code = cache.get(get_register_ver_code_pass_cache_key(ip))
    # if is_valid_ver_code:
    #     cache.delete(get_register_ver_code_pass_cache_key(ip))
    password = payload.password
    password_repeat = payload.password_repeat
    if password != password_repeat:
        return {'status_code': 500, 'message': '两次密码输入不一致，请重新输入'}
    email = payload.email
    ver_code = random.randint(100000, 999999)
    send_email_result = send_email(to_email=email, email_domain_prefix="onboarding", title='感谢注册', message=f'您的注册码是:{str(ver_code)}')
    if send_email_result:
        await cache.set(key=get_email_cache_key(email=email, type='register'), value=ver_code, timeout=600)
        email_signed = signing.dumps({'email': email})
        print(email_signed)
        user = user_dal.model(nick_name=payload.nick_name, email=email)
        user.set_password(payload.password)
        await save_user(user)
        return {'status_code': 200, 'message': '提交注册成功', 'email_signed': email_signed}
    return {'status_code': 400, 'message': '发生错误'}


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