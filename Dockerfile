FROM python:3.10

WORKDIR /zodiac

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "zodiac.asgi:application", "--host", "0.0.0.0", "--port", "80"]

