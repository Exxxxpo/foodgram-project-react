![status workflow](https://github.com/Exxxxpo/foodgram-project-react/actions/workflows/yamdb_workflow.yml/badge.svg)

# Информация для ревьюера: (на данный момент неактуально)

Адрес сайта: 
Данные для входа в админку:
login: 
pass: 22

# Описание проекта:

Проект *Foodgram* позволяет пользователям публиковать рецепты, подписываться
на публикации других пользователей, добавлять понравившиеся рецепты в список 
«Избранное», а перед походом в магазин скачивать сводный список продуктов, 
необходимых для приготовления одного или нескольких выбранных блюд.

Наш сервис позволяет:

* Создавать учётные записи
* Работать с учётными записями пользователей (получение, изменение данных, удаление аккаунта)
* Добавлять, редактировать, удалять, получать рецепт, тэг, ингридиенты.

## Инструкция по запуску:
Для начала создайте файл .env, затем отредактируйте:
```
cp infra/.env.template infra/.env 

```
Для загрузки фикстур в базу данных выполните:
```
sudo docker-compose exec backend python manage.py loaddata fixtures
```
Сборка образов и запуск контейнеров:
```
sudo docker-compose up - собрать все образы и запустить все контейнеры 
sudo docker-compose exec backend python manage.py migrate - выполнить миграции
sudo docker-compose exec backend python manage.py createsuperuser - создать суперпользователя
sudo docker-compose exec backend python manage.py collectstatic --no-input - собрать статику
```

## Использованные технологии:

* Python 3.7
* Django 3.2
* DjangoRestFramework 3.12.4
* Gunicorn 20.0.4
* Docker 3.8
* Nginx 1.21

### Автор

- Деваев Лев
