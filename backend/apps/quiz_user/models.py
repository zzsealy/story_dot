from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class QuizUser(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        error_messages={
            "unique": "用户名重复",
        },
    )
    password = models.CharField(help_text='密码', max_length=100)
    create_datetime = models.DateTimeField(auto_now_add=True, help_text='创建时间')

    class Meta:
        db_table = 'quiz_user'


