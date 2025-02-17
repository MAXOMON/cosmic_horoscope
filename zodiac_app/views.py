from django.shortcuts import render
from .models import ZodiacSign
from asgiref.sync import sync_to_async
from .utils import fetch_horoscope


@sync_to_async
def get_all_zodiac_signs():
    return list(ZodiacSign.objects.all())

async def index(request):
    main_data = await get_all_zodiac_signs()
    return render(
        request,
        template_name='index.html',
        context={'title': 'Ваш гороскоп - все знаки зодиака',
                 'main_data': main_data}
    )

@sync_to_async
def get_zodiac_data(zodiac_name):
    return ZodiacSign.objects.get(zodiac_en=zodiac_name)

async def zodiac(request, zodiac_name):
    zodiac_data = await get_zodiac_data(zodiac_name)
    html_description = await fetch_horoscope(zodiac_name)
    return render(request, 'zodiac_page.html',
                  {'title': zodiac_name, 'zodiac_data': zodiac_data,
                   'html_description': html_description})
