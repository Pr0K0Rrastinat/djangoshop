#!/bin/sh

# Применение миграций базы данных
python manage.py migrate

# Сбор статики
python manage.py collectstatic --noinput

# Запуск сервера
exec "$@"
