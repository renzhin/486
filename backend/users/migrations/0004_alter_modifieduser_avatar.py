# Generated by Django 3.2.16 on 2024-03-19 05:58

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_modifieduser_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modifieduser',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to=users.models.user_directory_path, verbose_name='Аватар'),
        ),
    ]
