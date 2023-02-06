![example workflow](https://github.com/Fedoska48/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

# 158.160.45.98
158.160.45.98/admin - панель администратора

158.160.45.98/api/docs/ - документация

# Проект Foodgram
Сайт Foodgram, «Продуктовый помощник». Онлайн-сервис и API для него. На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

# Технологический стек

* Django 3.2.16
* djangorestframework 3.14.0
* djoser 2.1.0
* drf-extra-fields 3.4.1
* gunicorn 20.1.0
* Pillow 9.3.0
* psycopg2-binary 2.9.5
* python-dotenv 0.21.0
* requests 2.28.1

# Установка
* Клонирование репозитория:

git clone git@github.com:Fedoska48/foodgram-project-react.git

Предварительно необходимо установить docker и docker-compose.

Из папки где находится файл docker-compose.yml необходимо запустить docker-compose:

docker-compose up -d --build

Выполните миграции:

docker-compose exec backend python manage.py migrate

Создайте суперпользователя:

docker-compose exec backend python manage.py createsuperuser

Сбор статики статику:

docker-compose exec backend python manage.py collectstatic --no-input

Импорт ингредиентов и тегов:

docker-compose exec backend python manage.py import_ingredients

docker-compose exec backend python manage.py import_tags

Остановка проекта:

docker-compose down

# Foodgram подволяет работать со следующими сущностями:

- Рецепты
- Теги
- Ингредиенты
- Пользователи

Автор [Fedoska48](https://github.com/Fedoska48)

41 когорта Яндекс.Практикум (Бекенд на Python)
