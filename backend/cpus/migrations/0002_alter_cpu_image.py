# Generated by Django 3.2.16 on 2024-03-04 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cpus', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cpu',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='cpus/'),
        ),
    ]