import httpx
import os
import pytz
from dotenv import load_dotenv
from .models import Weather, append_weather, get_weather
from datetime import timedelta
from django.utils.timezone import datetime



async def async_get_weather(city="St. Petersburg"):
    result = await get_weather()
    timezone = pytz.timezone('Europe/Moscow')
    if (datetime.now(timezone) - result.date) < timedelta(minutes=15):
        return result
    else:
        async with httpx.AsyncClient() as client:
            load_dotenv()
            url = os.getenv("URL")
            appid = os.getenv("APPID")
            response = await client.get(
                    url=url,
                    params={'q': city, "APPID": appid}
                )
            weather_json = response.json()
            await append_weather(weather_json)
            result = await get_weather()
            return result
