from django.db import models
from .zodiac_signs import zodiac_data

class ZodiacSign(models.Model):
    zodiac_ru = models.CharField(max_length=50, unique=True)
    zodiac_en = models.CharField(max_length=50, unique=True)
    start_day = models.CharField(max_length=20, unique=True)
    end_day = models.CharField(max_length=20, unique=True)
    svg = models.TextField()

    def __str__(self):
        return self.zodiac_en

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
