import random
import asyncio
from datetime import datetime
from asgiref.sync import sync_to_async

from django.core.cache import cache
from utils.email_utils import send_email, get_email_cache_key
from ninja import Router, Schema, ModelSchema, Field
# from .captcha_view import get_register_ver_code_pass_cache_key
from apps.customer_user.customer_user_dal import customer_user_dal
from utils.token_utils import generation_token
from django.contrib.auth.hashers import make_password, check_password

router = Router()

"""
注册
"""
class RegisterOut(Schema):
    code: int
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
        return {'code': 500, 'message': '两次密码输入不一致，请重新输入'}
    email = payload.email
    exist_user = quiz_user_dal.get_one_by_condition(condition={'username': email})
    if exist_user:
        return {'code': 500, 'message': '邮箱已经存在'}
    if '@' not in email:
        return {'code': 500, 'message': '邮箱格式不正确, 请重新输入'}
    

    email = payload.email
    cache_code = cache.get(get_email_cache_key(email=email, type='register'))
    if cache_code is None:
        return {'code': 500, 'message':'验证码不存在，请重新发验证码'}
    input_code = payload.ver_code
    if cache_code != input_code:
        return {'code':500, 'message':'验证码错误请重新输入'}
    else:
        cache.delete(get_email_cache_key(email, type='register'))
        password = make_password(payload.password)
        user = quiz_user_dal.model(username=email, password=password, create_datetime=datetime.now())
        user.save()
        return {'code': 200, 'message': '提交注册成功'}


"""
登录 
"""
class LoginSchema(Schema):
    # 其实alias是实际要传递的参数
    email: str = Field(alias='email')
    password: str = Field(alias='password')

class LoginOut(Schema):
    code: int
    token: str = None
    message: str

@router.post('/login', response=LoginOut, auth=None)
def login(request, payload: LoginSchema):
    try:
        quiz_user = quiz_user_dal.get_one_by_condition(condition={'username': payload.email})
        if quiz_user is None:
            return {'code': 500, 'message': '邮箱未注册，请先注册'}
        if check_password(payload.password, quiz_user.get('password')):
            return {'code': 200, 'message': '登录成功', 'token': generation_token(quiz_user.get('id'))}
        else:
            return {'code': 500, 'message': '密码不正确，请重试'}
    except Exception as e:
        return {'code': 400, 'message': '发生错误'}