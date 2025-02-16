from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    email = models.CharField(help_text='邮箱', max_length=100)
    password = models.CharField(help_text='密码', max_length=100)
    nick_name = models.CharField(help_text='昵称', max_length=100)
    create_datetime = models.DateTimeField(auto_now_add=True, help_text='创建时间')
    status = models.SmallIntegerField(default=0, help_text='0: 只是提交, 1: 注册成功, 验证通过')

    class Meta:
        db_table = 'user'


