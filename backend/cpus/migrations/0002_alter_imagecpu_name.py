# Generated by Django 3.2.16 on 2024-03-18 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cpus', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagecpu',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='название изображения'),
        ),
    ]
