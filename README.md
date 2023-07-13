## Проект YaMDb

Учебный командный проект YaMDb с реализацией API.
В проекте реализован функционал оценки и написания отзывов о различных произведений (книги, музыка, фильмы).

Возможности:

Наполнение базы данных из внешних источников (файлы .csv);
Регистрация и аутентификация пользователей с помощью e-mail и генерации токена;
Разделение пользователей по ролям доступа (админ, модератор, рядовой пользователь);
Создание пользователями отзывов на произведения и комментариев к ним;
Формирование рейтинга произведений по оценкам пользователей.

## Использованные технологии: 
* Python 3.9
* Django Rest Framework
  - Django-filter
  - Simple JWT
* SQLite
***

## Установка
#### Склонируйте репозиторий: 

```sh
git clone git@github.com:Gleb-Preob/api_yamdb.git
```
#### Находясь в папке с кодом создайте виртуальное окружение: 

```sh
python -m venv venv
```
#### Активируйте виртуальное окружение:

```sh
# для Windows
source venv\scripts\activate
# для Lunix и MacOS:
source venv/bin/activate
```

#### Установите зависимости: 

```sh
python -m pip install -r requirements.txt
```
#### Для заполнения базы данных выполните команду:

```sh
python manage.py import_csv
```

#### Для запуска сервера выполните команды:

```sh
python manage.py migrate
```
```sh
python manage.py createsuperuser
```
```sh
python manage.py runserver
```

## Техническое описание

http://127.0.0.1:8000/redoc/

   ```bash
   # запустить для Lunix и MacOS:
   xdg-open http://127.0.0.1:8000/redoc/
   ```

## Авторы
[AliceBolgarina](https://github.com/AliceBolgarina):
- произведения, категории, жанры, импорт файлов из csv

[Gleb-Preob](https://github.com/Gleb-Preob)
- отзывы, рейтинги, комментарии

[deeramster](https://github.com/deeramster)
- регистрация и аутентификация, пользователи