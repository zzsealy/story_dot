import random
import asyncio
from datetime import datetime

from django.core import signing
from django.db import IntegrityError
from asgiref.sync import sync_to_async

from django.core.cache import cache
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

class RegisterSchema(Schema):
    email: str = Field(description='邮箱')
    password: str = Field(description='密码')
    password_repeat: str = Field(description='重复密码')
    ver_code: int = Field(description='邮箱验证码')


@router.post('/register', response=RegisterOut)
def register(request, payload: RegisterSchema):
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
    exist_user = user_dal.get_one_by_condition(condition={'username': email})
    if exist_user:
        return {'status_code': 500, 'message': '邮箱已经存在'}
    if '@' not in email:
        return {'status_code': 500, 'message': '邮箱格式不正确, 请重新输入'}
    

    email = payload.email
    cache_code = cache.get(get_email_cache_key(email=email, type='register'))
    if cache_code is None:
        return {'status_code': 500, 'message':'验证码不存在，请重新发验证码'}
    input_code = payload.ver_code
    if cache_code != input_code:
        return {'status_code':500, 'message':'验证码错误请重新输入'}
    else:
        cache.delete(get_email_cache_key(email, type='register'))
        user = user_dal.model(username=email, create_datetime=datetime.now())
        user.set_password(payload.password)
        user.save()
        return {'status_code': 200, 'message': '提交注册成功'}


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