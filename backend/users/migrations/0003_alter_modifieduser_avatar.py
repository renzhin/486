# Generated by Django 3.2.16 on 2024-03-19 05:53

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20240318_2154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modifieduser',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to=users.models.user_directory_path),
        ),
    ]
