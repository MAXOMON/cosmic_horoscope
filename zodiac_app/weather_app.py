import time
import httpx
import os
from dotenv import load_dotenv
from .models import append_weather
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


async def async_add_weather(city="Murino"):
    async with httpx.AsyncClient(timeout=300) as client:
        load_dotenv()
        url = os.getenv("URL")
        appid = os.getenv("APPID")
        lat = cities[city]['lat']
        lon = cities[city]['lon']
        units = "metric"
        lang = 'ru'
        while True:
            response = await client.get(
                    url=url,
                    params={'lat': lat, 'lon': lon, "APPID": appid, 'units': units, 'lang': lang}
                )
            if response.status_code == 200:
                break
            time.sleep(1)
        weather_json = response.json()
        await append_weather(weather_json)
