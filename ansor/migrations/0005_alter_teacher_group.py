# Generated by Django 4.1.7 on 2023-02-25 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ansor', '0004_alter_customuser_is_student'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='group',
            field=models.ManyToManyField(null=True, to='ansor.group'),
        ),
    ]
