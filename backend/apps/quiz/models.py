from django.db import models

from apps.quiz_user.models import QuizUser

# Create your models here.

class QuizCategory(models.Model):
    name = models.CharField(max_length=50, verbose_name='题目分类')
    quiz_user = models.ForeignKey(
        QuizUser,
        on_delete=models.CASCADE,
        verbose_name='作者',
        related_name='quiz_categories'
    )
    create_datetime = models.DateTimeField(auto_now_add=True, help_text='创建时间')
    is_del = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'quiz_category'


class Quiz(models.Model):
    user = models.ForeignKey(
        QuizUser,
        on_delete=models.CASCADE,
        verbose_name='作者',
        related_name='quiz_s'
    )
    quiz_category = models.ForeignKey(
        QuizCategory,
        on_delete=models.CASCADE,
        verbose_name='分类',
        related_name='quiz_s'
    )
    question = models.TextField()
    answer_text = models.TextField(null=True, blank=True)
    answer_image_url = models.CharField(max_length=200, null=True, blank=True)
    create_datetime = models.DateTimeField(auto_now_add=True, help_text='创建时间')
    is_del = models.SmallIntegerField(default=0)

    class Meta:
        db_table = 'quiz'


class QuizChoice(models.Model):
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        verbose_name='题目',
        related_name='choices'
    )
    choice = models.CharField(max_length=200)
    is_true = models.BooleanField(default=False)


    class Meta:
        db_table = 'quiz_choice'