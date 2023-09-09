![status workflow](https://github.com/Exxxxpo/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

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

## Скриншоты
![image](https://github.com/Exxxxpo/foodgram-project-react/assets/102860715/d88399cf-3155-4393-b350-468b30a72952)
![image](https://github.com/Exxxxpo/foodgram-project-react/assets/102860715/749a86d6-2c8b-4e86-a853-5f66cf91211a)
![image](https://github.com/Exxxxpo/foodgram-project-react/assets/102860715/405e1b70-0d67-4870-a673-74c557d0c494)
![image](https://github.com/Exxxxpo/foodgram-project-react/assets/102860715/df9b9d94-5821-4b8e-ab07-efc3808c66fa)


### Автор

- Деваев Лев
