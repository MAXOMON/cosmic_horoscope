from django.core.management.base import BaseCommand
from ...models import ZodiacSign, Weather
from ...zodiac_signs import zodiac_data


class Command(BaseCommand):
    help = 'Заполняет БД первичными данными'

    def handle(self, *args, **options):
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
        Weather.objects.create(
            main="Данных нет",
            description="первичное заполнение",
            icon="50n",
            temperature=30.0,
            feels_like=35.0,
            pressure=1000,
            humidity=50,
            wind_speed=1,
            wind_degrees=180
        )
