import random

from django.core import signing 
from django.core.cache import cache
from django_ratelimit.decorators import ratelimit
from asgiref.sync import sync_to_async
from ninja import Router, Schema, ModelSchema, Field


from utils.email_utils import send_email, get_email_cache_key


router = Router()

class ValidEmailCodeOut(Schema):
    status_code: int
    message: str

class ValidEmailSchema(Schema):
    email: str
    email_code: int


@router.post('/valid_email_code', response=ValidEmailCodeOut)
async def valid_email_code(request, payload:ValidEmailSchema):
    email = ValidEmailSchema.email
    cache_code = cache.get(get_email_cache_key(email=email, type='register'))
    if cache_code is None:
        return {'status_code': 500, 'message':'验证码不存在，请重新发验证码'}
    input_code = payload.email_code
    if cache_code == input_code:
        await cache.delete(get_email_cache_key(email, type='register'))
        return {'status_code': 200, 'message': '注册成功'}
    else:
        return {'status_code':500, 'message':'验证码错误请重新输入'}


class SendEmailCodeOut(Schema):
    status_code: int
    message: str


class SendEmailSchema(Schema):
    email: str

@ratelimit(key='ip', rate='5/m')
@router.post('/send_email_code', response=SendEmailCodeOut)
def send_email_code(request, payload: SendEmailSchema):
    email = payload.email
    exist_email_code = cache.get(key=get_email_cache_key(email=email, type='register'))
    if exist_email_code:
        return {'satus_code': 500, 'message': '您已经发送邮件啦，请不要重复发送！'}
    ver_code = random.randint(100000, 999999)
    send_email_result = send_email(to_email=email, email_domain_prefix="onboarding", title='感谢注册', message=f'您的注册码是:{str(ver_code)}')
    if send_email_result:
        cache.set(key=get_email_cache_key(email=email, type='register'), value=ver_code, timeout=600)
        return {'status_code': 200, 'message': '发送成功'}
    return {'status_code': 500, 'message': '发生一些问题，请稍后重试'}
    