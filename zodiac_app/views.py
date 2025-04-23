from django.template.response import TemplateResponse
from .models import get_zodiac_data, get_weather, get_all_zodiac_signs
from django.views import View



class AsyncIndexView(View):
    async def get(self, request, *args, **kwargs):
        main_data = await get_all_zodiac_signs()
        weather_data = await get_weather()
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
        html_description = zodiac_data.description
        return TemplateResponse(request, 'zodiac_page.html',
                  {'title': zodiac_name, 'zodiac_data': zodiac_data,
                   'html_description': html_description})
