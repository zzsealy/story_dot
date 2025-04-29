from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from .serializers import UserSerializer, UserLoginSerializer
from utils.constants.status_code import StatusCode
import random

from django.core.cache import cache
from django_ratelimit.decorators import ratelimit
from apps.customer_user.customer_user_dal import customer_user_dal

from utils.email_utils import send_email, get_email_cache_key



"""
我们只想将用户展示成只读视图，
因此我们将使用ListAPIview和RetryeveAPIView通用的
基于类的视图
"""

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserRegister(APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user_instance = serializer.create(validated_data=serializer.validated_data)
            if user_instance:
                return Response( data={ "status_code": StatusCode.OK.value, "message": "注册成功, 请登录"})
            else:
                return Response( data={ "status_code": StatusCode.ERROR.value, "message": '发生错误'})
        else:
            return Response( data={ "status_code": serializer.error_code, "message": serializer.error_message })
    

class LoginView(APIView):
    
    def post(self, request):
        """
        **status_code**
        4004 邮箱不存在
        4003 密码不对
        """
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid():
            return Response(data={'status_code': StatusCode.OK.value, 'message': '登陆成功', 'token': serializer.validated_data})
        else:
            return Response( data={"status_code": serializer.error_code, 'message': serializer.error_message })


class UserInfo(APIView):
    
    def get(self, request):
        user_id = request.user_id
        user = User.objects.get(id=user_id)
        return Response(data={'status_code':StatusCode.OK.value, 'id':user.id, 'name': user.nick_name})




class valid_email_code(APIView):
    def get(self, request):
        email = request.query_params.get('email')
        cache_code = cache.get(get_email_cache_key(email=email, type='register'))
        if cache_code is None:
            return Response(data={'code': 501})
        input_code = request.query_params.get('email_code')
        if cache_code == input_code:
            cache.delete(get_email_cache_key(email, type='register'))
            return Response(data={'code': 200})
        else:
            return Response(data={'code':502})



@ratelimit(key='ip', rate='5/m')
class SendEmailCode(APIView):
    def post(self, request):
        send_type = request.data.get('send_type', 'register')
        email = request.data.get('email')
        if send_type == 'register':
            exist_user = customer_user_dal.get_one_by_condition(condition={'username': email})
            if exist_user:    # 邮箱存在
                return Response(data={'code': 503})
        exist_email_code = cache.get(key=get_email_cache_key(email=email, type='register'))
        if exist_email_code:
            return Response(data={'code': 504})
        ver_code = random.randint(100000, 999999)
        send_email_result = send_email(to_email=email, email_domain_prefix="onboarding", title='感谢注册', message=f'您的注册码是:{str(ver_code)}')
        if send_email_result:
            cache.set(key=get_email_cache_key(email=email, type='register'), value=ver_code, timeout=600)
            return Response(data={'code': 200})
        return Response(data={'code': 500})