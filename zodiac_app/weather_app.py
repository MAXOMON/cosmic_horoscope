import httpx
import os
import pytz
from dotenv import load_dotenv
from .models import Weather, append_weather, get_weather
from datetime import timedelta
from django.utils.timezone import datetime


cities = {
    "St. Petersburg": {
        "lat": 59.938732,
        "lon": 30.316229
        },
    "Murino": {
        "lat": 60.0494,
        "lon": 30.4459
        }
    }


async def async_get_weather(city="Murino"):
    result = await get_weather()
    timezone = pytz.timezone('Europe/Moscow')
    if (datetime.now(timezone) - result.date) < timedelta(minutes=15):
        return result
    else:
        async with httpx.AsyncClient() as client:
            load_dotenv()
            url = os.getenv("URL")
            appid = os.getenv("APPID")
            lat = cities[city]['lat']
            lon = cities[city]['lon']
            units = "metric"
            lang = 'ru'
            response = await client.get(
                    url=url,
                    params={'lat': lat, 'lon': lon, "APPID": appid, 'units': units, 'lang': lang}
                )
            weather_json = response.json()
            await append_weather(weather_json)
            result = await get_weather()
            return result
