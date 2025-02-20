from django.utils.timezone import now
from django.db import models, connection, transaction
from .zodiac_signs import zodiac_data


class ZodiacSign(models.Model):
    zodiac_ru = models.CharField(max_length=50, unique=True)
    zodiac_en = models.CharField(max_length=50, unique=True)
    start_day = models.CharField(max_length=20, unique=True)
    end_day = models.CharField(max_length=20, unique=True)
    svg = models.TextField()

    def __str__(self):
        return self.zodiac_en
    
    @classmethod
    def truncate(cls):
        with connection.cursor() as cursor:
            cursor.execute(f'TRUNCATE TABLE "{cls._meta.db_table}" CASCADE;')

def bulk_create_zodiac_signs():
    zodiac_signs = [
        ZodiacSign(
            zodiac_ru=data['zodiac_ru'],
            zodiac_en=data['zodiac_en'],
            start_day=data['start_day'],
            end_day=data['end_day'],
            svg=data['svg']
        ) for data in zodiac_data
    ]

    ZodiacSign.objects.abulk_create(zodiac_signs)


class Weather(models.Model):
    main = models.CharField(max_length=20)
    description = models.CharField(max_length=50)
    icon = models.CharField(max_length=20, default="50n")
    temperature = models.FloatField()
    feels_like = models.FloatField()
    pressure = models.IntegerField()
    humidity = models.IntegerField()
    wind_speed = models.IntegerField()
    wind_degrees = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.main

async def append_weather(weather_json):
    async with transaction.atomic():
        await Weather.objects.acreate(
            main=weather_json['weather'][0]['main'],
            description=weather_json['weather'][0]['description'],
            icon=weather_json['weather'][0]['icon'],
            temperature=weather_json['main']['temp'],
            feels_like=weather_json['main']['feels_like'],
            pressure=weather_json['main']['pressure'],
            humidity=weather_json['main']['humidity'],
            wind_speed=weather_json['wind']['speed'],
            wind_degrees=weather_json['wind']['deg']
            )

async def get_weather():
    result = await Weather.objects.alast()
    return result
