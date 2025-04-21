from datetime import datetime
from django.template.response import TemplateResponse
from .models import get_zodiac_data
from .utils import fetch_horoscope, get_all_signs
from .weather_app import async_get_weather
from django.views import View


class AsyncIndexView(View):
    async def get(self, request, *args, **kwargs):
        main_data = await get_all_signs()
        weather_data = await async_get_weather()
        return TemplateResponse(
            request,
            'index.html',
            context={
                'title': 'Ваш гороскоп - все знаки зодиака',
                'main_data': main_data,
                'weather_data': weather_data
            }
        )

class AsyncZodiacView(View):
    async def get(self, request, zodiac_name, *args, **kwargs):
        zodiac_data = await get_zodiac_data(zodiac_name)
        #html_description = await fetch_horoscope(zodiac_name)
        html_description = zodiac_data.description
        return TemplateResponse(request, 'zodiac_page.html',
                  {'title': zodiac_name, 'zodiac_data': zodiac_data,
                   'html_description': html_description})
