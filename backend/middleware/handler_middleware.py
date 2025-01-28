import json, time
import datetime

from django.conf import settings
from django.utils.timezone import localtime
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from utils.login_status_utils import generation_token,  verify_bearer_token

class Middleware(MiddlewareMixin):

    def __call__(self, request, **kwargs):
        login_verify_status = self.verify_login_validity(request)
        request.user_id = login_verify_status['user_id']  # 成功就返回用户的user 否则返回用户的
        if login_verify_status['result'] is False:
            return JsonResponse({'status_code': 401})
        response = self.get_response(request)
        return response
        # return JsonResponse(data={"susscess":0, "message":"记录事件开始到数据库出错"}, content_type='application/json', status=401)

    
    def verify_login_validity(self, request):
        token_key = request.META.get('HTTP_AUTHORIZATION', None)
        if '/captcha.image/' in request.path:
            request_path = '/captcha.image/'
        else:
            request_path = request.path
        url_info = settings.AUTHENTICATION_SKIP_URL.get(request_path)
        status = self.verify_bearer_token(token_key=token_key)
        if url_info and request.method in url_info:
            # 如果url在忽略token验证的路由和方法里，就不进行token验证
            status['result'] = True
        
        return status
    

    def verify_bearer_token(self, token_key):
        if not token_key:
            return {'user_id': None, 'result': False}
        token = token_key.split(' ')[1]
        result = verify_bearer_token(token=token)
        if result:
            is_expire = self.checkout_token_time(result.get('exp_time'))
            if not is_expire:  # 没过期
                return {'user_id': result.get('user_id'), 'result': True}
            return {'user_id': None, 'result': False}
        else:
            return {'user_id': None, 'result': False}
    

    def checkout_token_time(self, exp_time):
        if exp_time > (time.time()):
            return False
        return True