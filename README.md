# Как установить

1. Установите Docker и Docker-compose;
2. Клонируйте репозиторий или скопируйте файлы;

    # Dockerfile:

    >```Dockerfile
    >FROM python:3.11
    >
    >ENV PYTHONDONTWRITEBYTECODE=1
    >
    >ENV PYTHONUNBUFFERED=1
    >
    >WORKDIR /zodiac
    >
    >COPY requirements.txt .
    >
    >RUN pip install --no-cache-dir -r requirements.txt
    >
    >COPY . .
    >
    >EXPOSE 8000
    >
    >CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "zodiac.asgi:application", "--bind", "0.0.0.0:8000"]
    >

3. Настройте .env файл;

    >```
    >
    >URL = 'http://api.openweathermap.org/data/2.5/weather'
    >APPID = "Ваш API token от сервиса openweathermap"
    >SECRET_KEY = "Django SECRET_KEY" 
    Django secret key можно получить подобным образом:
    ```python
    >python -c 'import random'
    >result = "".join([random.choice("abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)") for i in range(50)])

4. Настройте docker-compose.yml
    >```
    >
    >services:
    >web:
    >    build: .
    >    command: ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "zodiac.asgi:application", "--bind", "0.0.0.0:8000"]
    >    volumes:
    >    - .:/zodiac
    >    ports:
    >    - "8000:8000"
    >    depends_on:
    >    - redis
    >    - celery
    >    - celery-beat
    >
    >redis:
    >    image: "redis:alpine"
    >    ports:
    >    - "6379:6379"
    >
    >celery:
    >    build: .
    >    command: ["celery", "-A", "zodiac", "worker", "--loglevel=info"]
    >    volumes:
    >    - .:/zodiac
    >    depends_on:
    >    - redis
    >    
    >celery-beat:
    >    build: .
    >    command: ["celery", "-A", "zodiac", "beat", "--loglevel=info"]
    >    volumes:
    >    - .:/zodiac
    >    depends_on:
    >    - redis

5. Запустите приложение с использованием docker-compose:
    >```cmd
    >docker compose up --build

# Переходим на localhost:8000/ и получаем:

![img](./readme_images/image.png)
