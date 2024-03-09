import json
from datetime import datetime

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from cpu_backend import settings
from cpus.models import Cpu, Manufacturer

User = get_user_model()


class Command(BaseCommand):
    help = 'Импортирование даты JSON в модель Джанго'

    def handle(self, *args, **options):
        data_path = settings.BASE_DIR

        self.stdout.write(self.style.SUCCESS('Импортирование данных v.1...'))

        with open(
            f'{data_path}/data/cpus.json', 'r', encoding='utf-8'
        ) as file:
            data = json.load(file)

            for item in data:
                # Преобразование строки даты в объект даты py
                purchase_date_str = item.pop('purchase_date')
                purchase_date = datetime.strptime(
                    purchase_date_str, '%Y-%m-%d'
                ).date()
                item['purchase_date'] = purchase_date

                # Получаем или создаем экземпляр модели Manufacturer
                mnf_inst, created = Manufacturer.objects.get_or_create(
                    name=item['manufacturer']
                )
                item['manufacturer'] = mnf_inst

                # Получаем экземпляр модели User
                user_inst = User.objects.get(
                    username=item['user']
                )
                item['user'] = user_inst
                # Создаем экземпляр модели Cpu и сохраняем его
                ingredient_instance = Cpu(**item)
                ingredient_instance.save()

        self.stdout.write(
            self.style.SUCCESS('Импортирование процессоров завершено.')
        )
