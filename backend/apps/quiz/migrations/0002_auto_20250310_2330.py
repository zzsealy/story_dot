# Generated by Django 3.2 on 2025-03-10 23:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='quiz',
            table='quiz',
        ),
        migrations.AlterModelTable(
            name='quizcategory',
            table='quiz_category',
        ),
        migrations.AlterModelTable(
            name='quizchoice',
            table='quiz_choice',
        ),
    ]
