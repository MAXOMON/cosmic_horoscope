FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

WORKDIR /zodiac

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

RUN python manage.py loaddata zodiac_app/fixtures/zodiac_app.json --app zodiac_app

CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "zodiac.asgi:application", "--bind", "0.0.0.0:8000"]