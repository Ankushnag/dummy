# Generated by Django 4.0.3 on 2022-10-19 07:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_pasword2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='pasword2',
        ),
    ]