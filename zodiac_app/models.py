from django.utils.timezone import now
from django.db import models, connection
from .zodiac_signs import zodiac_data
from asgiref.sync import sync_to_async



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

    ZodiacSign.objects.bulk_create(zodiac_signs)


class Weather(models.Model):
    main = models.CharField(max_length=20)
    description = models.CharField(max_length=50, null=True, blank=True, default=None)
    temperature = models.FloatField(null=False)
    feels_like = models.FloatField(null=True, blank=True, default=None)
    pressure = models.IntegerField()
    humidity = models.IntegerField()
    wind_speed = models.IntegerField()
    wind_degrees = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.main

@sync_to_async
def append_weather(weather_json):
    Weather.objects.create(
            main=weather_json['weather'][0]['main'],
            description=weather_json['weather'][0]['description'],
            temperature=weather_json['main']['temp'],
            feels_like=weather_json['main']['feels_like'],
            pressure=weather_json['main']['pressure'],
            humidity=weather_json['main']['humidity'],
            wind_speed=weather_json['wind']['speed'],
            wind_degrees=weather_json['wind']['deg']
    )

@sync_to_async
def get_weather():
    return Weather.objects.last()
