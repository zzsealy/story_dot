import random

from django.core import signing 
from django.core.cache import cache
from django_ratelimit.decorators import ratelimit
from asgiref.sync import sync_to_async
from ninja import Router, Schema, ModelSchema, Field
from apps.customer_user.customer_user_dal import customer_user_dal

from utils.email_utils import send_email, get_email_cache_key


router = Router()

class ValidEmailCodeOut(Schema):
    code: int

class ValidEmailSchema(Schema):
    email: str
    email_code: int


@router.post('/valid_email_code', response=ValidEmailCodeOut)
async def valid_email_code(request, payload:ValidEmailSchema):
    email = ValidEmailSchema.email
    cache_code = cache.get(get_email_cache_key(email=email, type='register'))
    if cache_code is None:
        return {'code': 501}
    input_code = payload.email_code
    if cache_code == input_code:
        await cache.delete(get_email_cache_key(email, type='register'))
        return {'code': 200}
    else:
        return {'code':502}


class SendEmailCodeOut(Schema):
    code: int
    message: str


class SendEmailSchema(Schema):
    email: str
    send_type: int = None

@ratelimit(key='ip', rate='5/m')
@router.post('/send_email_code', response=SendEmailCodeOut)
def send_email_code(request, payload: SendEmailSchema):
    send_type = payload.send_type if payload.send_type else 'register' 
    email = payload.email
    if send_type == 'register':
        exist_user = customer_user_dal.get_one_by_condition(condition={'username': email})
        if exist_user:    # 邮箱存在
            return {'code': 503}
    exist_email_code = cache.get(key=get_email_cache_key(email=email, type='register'))
    if exist_email_code:
        return {'code': 504}
    ver_code = random.randint(100000, 999999)
    send_email_result = send_email(to_email=email, email_domain_prefix="onboarding", title='感谢注册', message=f'您的注册码是:{str(ver_code)}')
    if send_email_result:
        cache.set(key=get_email_cache_key(email=email, type='register'), value=ver_code, timeout=600)
        return {'code': 200}
    return {'code': 500}
    