![status workflow](https://github.com/Exxxxpo/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

# Информация для ревьюера:

Адрес сайта: http://158.160.19.246/
Данные для входа в админку:
login: admin
pass: 1


# Описание проекта:

Проект *Foodgram* позволяет пользователям публиковать рецепты, подписываться
на публикации других пользователей, добавлять понравившиеся рецепты в список
«Избранное», а перед походом в магазин скачивать сводный список продуктов,
необходимых для приготовления одного или нескольких выбранных блюд.

Наш сервис позволяет:

* Создавать учётные записи
* Работать с учётными записями пользователей (получение, изменение данных, удаление аккаунта)
* Добавлять, редактировать, удалять, получать рецепт, тэг, ингридиенты.
* Скачивать список ингридиентов необходимых для приготовления блюда.

## Инструкция по запуску:
Для начала создайте файл .env, затем отредактируйте:
```
cp infra/.env.template infra/.env
```
Сборка образов и запуск контейнеров:
```
sudo docker-compose up -d собрать все образы и запустить все контейнеры
sudo docker-compose exec backend python manage.py migrate выполнить миграции
sudo docker-compose exec backend python manage.py createsuperuser создать суперпользователя
sudo docker-compose exec backend python manage.py collectstatic --no-input собрать статику
```

Для загрузки фикстур в базу данных выполните:
```
sudo docker-compose exec backend python manage.py loaddata fixtures
```

## Использованные технологии:

* Python 3.7
* pip 22.3.1
* Django 3.2
* DjangoRestFramework 3.12.4
* Djoser 2.1.0
* Docker 3.8
* Gunicorn 20.0.4
* Nginx 1.21
* Pillow 8.3.1
* Postgresql 12.14

### Автор

- Деваев Лев
