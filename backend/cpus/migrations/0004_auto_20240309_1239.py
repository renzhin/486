# Generated by Django 3.2.16 on 2024-03-09 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cpus', '0003_auto_20240309_0955'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cpu',
            name='purchase_date',
            field=models.DateField(verbose_name='дата покупки'),
        ),
        migrations.AlterField(
            model_name='cpu',
            name='sale_date',
            field=models.DateField(blank=True, null=True, verbose_name='дата продажи'),
        ),
    ]
