# Generated by Django 3.1.3 on 2020-11-25 13:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='manageraccount',
            name='manager',
        ),
        migrations.DeleteModel(
            name='ControllerAccount',
        ),
        migrations.DeleteModel(
            name='ManagerAccount',
        ),
    ]
