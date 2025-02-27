import string
import random
from django.conf import settings

import resend



resend.api_key = settings.RESEND_API_KEY

def send_email(to_email:str, email_domain_prefix: str, title: str, message: str) -> bool:
    r = resend.Emails.send({
    "from": f"{email_domain_prefix}@{settings.EMAIL_DOMAIN}",
    "to": to_email,
    "subject": title,
    "html": f"<p>{message}</p>"
    })

    id = r.get('id')
    if id:
        return True
    return False
    # return True


def get_email_cache_key(email: str, type: str) -> str:
    return f'email|{email}|{type}'


def generate_random_string(length=10):
    # 从字母和数字中随机选择
    characters = string.ascii_letters + string.digits  # 包含所有字母（大小写）和数字
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string