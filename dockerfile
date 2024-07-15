# Используем базовый образ Python
FROM python:3.12

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файлы проекта в контейнер
COPY . /app

# Устанавливаем зависимости
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Копируем и даем права на выполнение скрипта entrypoint.sh
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Запускаем скрипт entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]

# Определяем команду для запуска контейнера
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "djangoshop.wsgi:application"]
