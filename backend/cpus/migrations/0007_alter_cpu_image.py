# Generated by Django 3.2.16 on 2024-03-18 19:27

import cpus.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cpus', '0006_cpu_hidden_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cpu',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=cpus.models.user_directory_path),
        ),
    ]
