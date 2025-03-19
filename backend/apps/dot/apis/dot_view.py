
import random

from django.core import signing 
from django.core.cache import cache
from django_ratelimit.decorators import ratelimit
from asgiref.sync import sync_to_async
from ninja import Router, Schema, ModelSchema, Field
from apps.customer_user.customer_user_dal import customer_user_dal



router = Router()

class ValidEmailCodeOut(Schema):
    code: int
    message: str

# class ValidEmailSchema(Schema):
#     pass


@router.get('/get_story_dots', response=ValidEmailCodeOut)
def valid_email_code(request):
    user_id = request.user_id
    return {'code': 200, 'message': '注册成功'}
