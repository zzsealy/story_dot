import base64
import datetime
import json, time

from django.conf import settings
from django.utils.timezone import localtime
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from utils.login_status_utils import generation_token,  verify_bearer_token
from Crypto.Cipher import AES

class Middleware(MiddlewareMixin):

    def __call__(self, request, **kwargs):
        login_verify_status = self.verify_login_validity(request)
        request.user_id = login_verify_status['user_id']  # 成功就返回用户的user 否则返回用户的
        if login_verify_status['result'] is False:
            return JsonResponse({'status_code': 401})
        if request.method in ['POST', 'PUT', 'PATCH']:
            try:
                # 获取加密的 data 字段
                body_data = json.loads(request.body)
                encrypted_data = body_data.get('data')
                if encrypted_data:
                    # 解密数据
                    decrypted_data = self.decrypt_data(encrypted_data)
                    if decrypted_data:
                        # 将解密后的数据重新赋值给 request.POST 或 request.body
                        request._body = json.dumps(decrypted_data).encode('utf-8')
                        request.POST = request.POST.copy()
                        request.POST.update(decrypted_data)
                    else:
                        return JsonResponse({'status_code': 400, 'message': 'Invalid data'}, status=400)
            except json.JSONDecodeError:
                return JsonResponse({'status_code': 400, 'message': 'Invalid JSON'}, status=400)
        response = self.get_response(request)
        return response
        # return JsonResponse(data={"susscess":0, "message":"记录事件开始到数据库出错"}, content_type='application/json', status=401)
    
    # def decrypt_data(self, encrypted_data):
    #     """解密数据"""
    #     try:
    #         key = base64.b64decode(settings.ENCRYPTION_KEY)
    #         cipher = AES.new(key, AES.MODE_ECB)
    #         decrypted_data = cipher.decrypt(base64.b64decode(encrypted_data)).strip()
    #         decrypted_data = json.loads(decrypted_data.decode('utf-8'))
    #         return decrypted_data
    #     except Exception as e:
    #         print(f"Decryption failed: {e}")
    #         return None
        
    @staticmethod
    def unpad(data):
        """移除 PKCS7 填充字节"""
        pad_length = data[-1]
        return data[:-pad_length]

    def decrypt_data(self, encrypted_data):
        try:
            # 解码 Base64
            key = base64.b64decode(settings.ENCRYPTION_KEY)
            encrypted_bytes = base64.b64decode(encrypted_data)
            # 创建 AES 解密器
            cipher = AES.new(key, AES.MODE_ECB)
            # 解密数据
            decrypted_data = cipher.decrypt(encrypted_bytes)
            # 移除填充字节
            decrypted_data = self.unpad(decrypted_data)
            # 将字节数据转换为字符串并解析为 JSON
            return json.loads(decrypted_data.decode('utf-8'))
        except Exception as e:
            print(f"Decryption failed: {e}")
            return None
    
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