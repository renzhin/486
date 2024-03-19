# Generated by Django 3.2.16 on 2024-03-19 05:58

import cpus.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cpus', '0002_auto_20240319_0835'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagecpu',
            name='cpu',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='cpus.cpu', verbose_name='процессор'),
        ),
        migrations.AlterField(
            model_name='imagecpu',
            name='image',
            field=models.ImageField(upload_to=cpus.models.user_cpu_directory_path, verbose_name='фото процессора'),
        ),
    ]
