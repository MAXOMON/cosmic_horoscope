from django.db import models, connection
from asgiref.sync import sync_to_async


class ZodiacSign(models.Model):
    zodiac_ru = models.CharField(max_length=50, unique=True)
    zodiac_en = models.CharField(max_length=50, unique=True)
    start_day = models.CharField(max_length=20, unique=True)
    end_day = models.CharField(max_length=20, unique=True)
    last_updated = models.DateField(auto_now=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.zodiac_en
    
    @classmethod
    def truncate(cls):
        with connection.cursor() as cursor:
            cursor.execute(f'TRUNCATE TABLE "{cls._meta.db_table}" CASCADE;')

@sync_to_async
def get_all_zodiac_signs():
    return list(ZodiacSign.objects.all())

async def get_zodiac_data(zodiac_name):
    return await ZodiacSign.objects.aget(zodiac_en=zodiac_name)

async def add_description_to_horoscope_sign(zodiac_name, description: str):
    await ZodiacSign.objects.filter(zodiac_en=zodiac_name).aupdate(description=description)


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
