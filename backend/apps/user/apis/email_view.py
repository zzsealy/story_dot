from django.core import signing 
from asgiref.sync import sync_to_async
from ninja import Router, Schema, ModelSchema, Field

from utils.cache import cache
from utils.email_utils import get_email_cache_key


router = Router()

class ValidEmailCodeOut(Schema):
    status_code: int
    message: str
    user_id: int = None

class ValidEmailSchema(Schema):
    email_signed: str
    email_code: int


@router.post('/valid_email_code', response=ValidEmailCodeOut)
async def valid_email_code(request, payload:ValidEmailSchema):
    email_signed = payload.email_signed
    try:
        sign_dict = signing.loads(email_signed)
    except Exception as e:
        return {'status_code': 500, 'message':'验签失败'}
    email = sign_dict.get('email')
    cache_code = await cache.get(get_email_cache_key(email=email, type='register'))
    if cache_code is None:
        return {'status_code': 500, 'message':'验证码不存在，请重新发验证码'}
    input_code = payload.email_code
    if cache_code == input_code:
        user_id = 0
        await cache.delete(get_email_cache_key(email, type='register'))
        return {'status_code': 200, 'message': '注册成功', 'user_id': user_id}
    else:
        return {'status_code':400, 'message':'验证码错误请重新输入'}