1. Установите Docker и Docker Compose.

2. Клонируйте репозиторий или скопируйте файлы.

=================================================================================

#Dockerfile:

=================================================================================
FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

WORKDIR /zodiac

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "zodiac.asgi:application", "--host", "0.0.0.0", "--port", "8000"]
=================================================================================

#docker-compose.yml:

=================================================================================

services:
  db:
    image: postgres:13
    env_file:
      - .env
    hostname: ${DB_HOSTNAME}
    environment:
      POSTGRES_DB: ${DB_NAME}
      POSTGRES_USER: ${DB_USERNAME}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
  
  web:
    build: .
    command: uvicorn zodiac.asgi:application --host 0.0.0.0 --port 8000
    volumes:
      - .:/zodiac
    ports:
      - "8000:8000"
    depends_on:
      - db

volumes:
  postgres_data:
=================================================================================

3. Настройте .env файл.

=================================================================================
URL = 'http://api.openweathermap.org/data/2.5/weather'
APPID = "Ваш API token от сервиса openweathermap"
DB_HOSTNAME = 'Например, db'
DB_NAME = 'Например, zodiac'
DB_USERNAME = 'Например, zodiac_user'
DB_PASSWORD = 'Например, 321321baseTobase321321'
DB_PORT = 'Например, 5432'
=================================================================================

4. Запустите приложение с использованием docker-compose up.
