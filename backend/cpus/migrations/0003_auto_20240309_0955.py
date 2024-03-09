# Generated by Django 3.2.16 on 2024-03-09 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cpus', '0002_alter_cpu_image'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='cpu',
            name='uniq_cpu',
        ),
        migrations.RemoveField(
            model_name='cpu',
            name='name',
        ),
        migrations.RemoveField(
            model_name='cpu',
            name='price_description',
        ),
        migrations.AddField(
            model_name='cpu',
            name='catalog_number',
            field=models.CharField(blank=True, max_length=4, verbose_name='Номер в коллекции'),
        ),
        migrations.AddField(
            model_name='cpu',
            name='sale_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='дата продажи'),
        ),
        migrations.AlterField(
            model_name='cpu',
            name='rarity',
            field=models.CharField(choices=[('NN', 'Не задано'), ('CM', 'Частый'), ('UN', 'Нечастый'), ('RR', 'Редкий'), ('ER', 'Очень редкий')], default='NN', max_length=128, verbose_name='Редкость'),
        ),
        migrations.AlterField(
            model_name='cpu',
            name='work_status',
            field=models.CharField(choices=[('NT', 'Непроверенный'), ('WK', 'Рабочий'), ('DF', 'Неисправен'), ('OC', 'Разогнан')], default='NT', max_length=128, verbose_name='Статус'),
        ),
        migrations.AddConstraint(
            model_name='cpu',
            constraint=models.UniqueConstraint(fields=('catalog_number', 'user'), name='uniq_cpu'),
        ),
    ]