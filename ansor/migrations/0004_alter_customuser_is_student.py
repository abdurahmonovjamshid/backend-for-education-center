# Generated by Django 4.1.7 on 2023-02-25 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ansor', '0003_group_teacher_student'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='is_student',
            field=models.BooleanField(default=True),
        ),
    ]
