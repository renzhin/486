# Generated by Django 3.2.16 on 2024-03-18 20:10

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cpu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата добавления')),
                ('part_number', models.CharField(max_length=128, verbose_name='серийный номер')),
                ('catalog_number', models.CharField(blank=True, max_length=4, verbose_name='Номер в коллекции')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('hidden_description', models.TextField(blank=True, null=True, verbose_name='Скрытое описание')),
                ('work_status', models.CharField(choices=[('NT', 'Непроверенный'), ('WK', 'Рабочий'), ('DF', 'Неисправен'), ('OC', 'Разогнан')], default='NT', max_length=128, verbose_name='Статус')),
                ('rarity', models.CharField(choices=[('NN', 'Не задано'), ('CM', 'Частый'), ('UN', 'Нечастый'), ('RR', 'Редкий'), ('ER', 'Очень редкий')], default='NN', max_length=128, verbose_name='Редкость')),
                ('family', models.CharField(max_length=128, verbose_name='семейство')),
                ('frequency', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='частота процессора')),
                ('fsb', models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1)], verbose_name='частота шины')),
                ('multiplier', models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1)], verbose_name='множитель')),
                ('fpu', models.BooleanField(default=True, verbose_name='математический сопроцессор (FPU)')),
                ('l1_cache_size', models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1)], verbose_name='размер кеша L1')),
                ('vcore', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1)], verbose_name='напряжение ядра')),
                ('overclk_frequency', models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1)], verbose_name='частота в разгоне')),
                ('overclk_fsb', models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1)], verbose_name='частота шины в разгоне')),
                ('overclk_multiplier', models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1)], verbose_name='множитель в разгоне')),
                ('overclk_vcore', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1)], verbose_name='напряжение ядра в разгоне')),
                ('purchase_date', models.DateField(verbose_name='дата покупки')),
                ('purchase_price', models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Стоимость покупки')),
                ('sale_price', models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Стоимость продажи')),
                ('sale_date', models.DateField(blank=True, null=True, verbose_name='дата продажи')),
                ('is_published', models.BooleanField(default=True, help_text='Снимите галочку, чтобы скрыть публикацию.', verbose_name='Опубликовано')),
                ('in_interesting', models.BooleanField(default=False, help_text='Снимите галочку, чтобы скрыть с главной.', verbose_name='В интересном')),
            ],
            options={
                'verbose_name': 'процессор',
                'verbose_name_plural': 'Процессоры',
            },
        ),
        migrations.CreateModel(
            name='Manufacturer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата добавления')),
                ('name', models.CharField(max_length=128, verbose_name='тип')),
            ],
            options={
                'verbose_name': 'производитель',
                'verbose_name_plural': 'Производители',
            },
        ),
        migrations.CreateModel(
            name='ImageCpu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='название изображения')),
                ('image', models.ImageField(upload_to='cpus/')),
                ('default', models.BooleanField(default=False)),
                ('cpu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='cpus.cpu')),
            ],
        ),
        migrations.AddField(
            model_name='cpu',
            name='manufacturer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cpus', to='cpus.manufacturer', verbose_name='производитель'),
        ),
        migrations.AddField(
            model_name='cpu',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cpus', to=settings.AUTH_USER_MODEL, verbose_name='Владелец'),
        ),
        migrations.AddConstraint(
            model_name='cpu',
            constraint=models.UniqueConstraint(fields=('catalog_number', 'user'), name='uniq_cpu'),
        ),
    ]
