import json

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand
from django.db.models import Q

from cpu_backend import settings

User = get_user_model()


class Command(BaseCommand):
    help = 'Импортирование даты JSON в модели Джанго'

    def handle(self, *args, **options):
        data_path = settings.BASE_DIR

        self.stdout.write(self.style.SUCCESS('Импортирование данных v.1...'))

        with open(
            f'{data_path}/data/users.json', 'r', encoding='utf-8'
        ) as file:
            users_data = json.load(file)
            for item in users_data:
                existing_user = User.objects.filter(
                    Q(email=item['email']) |
                    Q(username=item['username'])
                ).first()
                if existing_user:
                    self.stdout.write(self.style.WARNING(
                        f'Пользователь с почтой "{item["email"]}" '
                        f'или username "{item["username"]}" уже в базе. '
                        'Пропускаем.'
                    ))
                    continue
                # Хешируем пароль
                item['password'] = make_password(item['password'])

                # Создаем экземпляр модели User и сохраняем его
                user_instance = User(**item)
                user_instance.save()

        self.stdout.write(
            self.style.SUCCESS('Импортирование пользователей завершено.')
        )
