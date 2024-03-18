# 486 - агрегатор коллекционера, собирающего процессоры 486 поколения
# Проект в разработке

## Веб-приложение, позволяющее каталогизировать имеющиеся в коллекции процессоры, а также собрать всю дополнительную информацию о возможностях разгона каждого экземпляра, на сколько он редок и за какую сумму и на какой площадке был куплен.

##  Автор
[@renzhin](https://github.com/renzhin)

## Используемые технологии
•   Python 3.9.18<br>
•   Django 3.2.16<br>
•   PostgreSQL(psycopg2 2.9.3)<br>
•   Bootstrap v5.0.2<br>


## Проект развернут по адресу:
https://486.renzhin.ru/


## Как запустить проект на удаленном сервере с помощью Docker на PostgreSQL:

Клонируем репозиторий:
````
git@github.com:renzhin/486.git
````

На виртуальном сервере создаем директорию проекта с именем 486/

Копируем в папку 486/ файл с переменными окружения .env и файл оркестрации контейнеров docker-compose.production.yml

Запускайем docker-compose.production.yml в режиме демона командой:
````
sudo docker compose -f docker-compose.production.yml up -d 
````

Собираем статику в контейнере backend:
````
sudo docker compose -f docker-compose.production.yml exec backend python manage.py collectstatic
````

Копируем собранную статику:
````
sudo docker compose -f docker-compose.production.yml exec backend cp -r /app/collected_static/. /backend_static/
````

Выполняем миграции:
````
sudo docker compose -f docker-compose.production.yml exec backend python manage.py migrate
````

Создаем суперпользователя:
````
sudo docker compose -f docker-compose.production.yml exec backend python manage.py createsuperuser
````

Загружаем фикстуры пользователей:
````
sudo docker compose -f docker-compose.production.yml exec backend python manage.py import_userss
````

Загружаем фикстуры процессоров:
````
sudo docker compose -f docker-compose.production.yml exec backend python manage.py import_cpus
````

Пример заполнения файла с переменными окружения.env:
````
# Файл .env
POSTGRES_DB=django
POSTGRES_USER=my_user
POSTGRES_PASSWORD=mysecretpassword
DB_NAME=my_db
# Добавляем переменные для Django-проекта:
DB_HOST=db
DB_PORT=5432
# Добавляем ключ в settings.py
SECRET_KEY=django-insecure-1234567891011121223321231232323232321323
# Режим отладки
DEBUG_MODE=False
# Адреса хостов
ALLOW_HOSTS='11.22.33.44 localhost 486.name.ru'
# Проброс порта Nginx
WEB_PORT=9876

````


## Как запустить проект локально на SQLite3:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:renzhin/486.git
```

```
cd 486
```

Cоздать и активировать виртуальное окружение в Windows:

```
python -m venv venv
```

```
source venv/Scripts/activate
```

Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

Создаем суперпользователя:
````
python manage.py createsuperuser
````

Загружаем фикстуры пользователей:
````
python manage.py import_users
````

Загружаем фикстуры процессоров:
````
python manage.py import_cpus
````

Запустить проект:

```
python manage.py runserver
```

### Пример заполнения файла с переменными окружения.env (локальный запуск):
````
SECRET_KEY=django-insecure-1234567891011121223321231232323232321323
ALLOWED_HOSTS='127.0.0.1'
DEBUG_MODE=True
````