import asyncio
from zodiac.celery import app
from celery import shared_task
from .models import get_all_zodiac_signs, add_description_to_horoscope_sign
from .utils import fetch_horoscope
from .weather_app import async_add_weather


@shared_task(name='update_zodiac_signs', default_retry_delay=15)
def update_zodiac_signs():
    async def process():
        all_signs = await get_all_zodiac_signs()
        names_of_signs = [it.zodiac_en for it in all_signs]
        new_data = {}
        for name in names_of_signs:
            new_data[name] = await asyncio.create_task(fetch_horoscope(name))

        for zodiac_sign, description in new_data.items():
            await add_description_to_horoscope_sign(
                zodiac_name=zodiac_sign,
                description=description
            )
    asyncio.run(process())
    return "success" 

@shared_task(name='update_weather', default_retry_delay=15)
def update_weather():
    async def process():
        await async_add_weather()
    asyncio.run(process())
    return "success" 
