# Generated by Django 3.1.3 on 2020-11-25 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='userCategoryType',
            field=models.TextField(default='customer', verbose_name='user_category_type'),
        ),
    ]
