import jwt
import time
from django.conf import settings


def generation_token(user_id: int) -> str:
    expire_time =  int(time.time()) + 3600*24*settings.TOKEN_AGE
    token = jwt.encode(
        payload={'user_id': user_id, 'exp_time': expire_time},
        key=settings.SECRET_KEY, 
        algorithm='HS256'
    )
    return token

def verify_bearer_token(token):
    result = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
    return result