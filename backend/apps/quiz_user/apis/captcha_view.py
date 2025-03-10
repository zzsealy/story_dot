# from ninja import Router, Schema, ModelSchema, Field
# from captcha.models import CaptchaStore
# from captcha.helpers import captcha_image_url

# from utils.cache import cache

# router = Router()

# def get_register_ver_code_pass_cache_key(ip):
#     return f'{ip}|register_ver_code_pass'

# # 获取人机验证码
# class GetCaptchaOut(Schema):
#     code: int
#     captcha_key: str
#     captcha_url: str

# @router.get('/get_captcha', response=GetCaptchaOut)
# def get_captcha(request):
#     captcha = CaptchaStore.generate_key()
#     captcha_url = captcha_image_url(captcha)
#     return {'code': 200, 'captcha_key': captcha, 'captcha_url': captcha_url}


# # 验证验证码
# class CaptchaValidationRequest(Schema):
#     captcha_key: str
#     ver_code: str # 用户输入的验证码

# # 验证验证码
# @router.post('/validate_captcha')
# def validate_captcha(request, payload: CaptchaValidationRequest):
#     try:
#         captcha = CaptchaStore.objects.get(hashkey=payload.captcha_key)
#         if captcha.response == payload.ver_code.lower():
#             ip = request.META.get('REMOTE_ADDR')
#             cache.set(get_register_ver_code_pass_cache_key(ip), True)
#             captcha.delete()
#             return {'code': 200, 'message': '验证码正确'}
#         else:
#             return {'code': 400, 'message': '验证码错误'}
#     except CaptchaStore.DoesNotExist:
#         return {'code': 400, 'message': '验证码无效'}


