import asyncio
from datetime import datetime
import httpx
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from .models import get_all_zodiac_signs, add_description_to_horoscope_sign


async def async_get_lines(text: str):
    for line in text:
        yield line

async def fetch_horoscope(zodiac_en='cancer'):
    # create Fake User Agent
    ua = UserAgent()
    headers = {
        'accept': '*/*',
        'accept-language': 'ru,en;q=0.9',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'priority': 'u=0, i',
        'referer': 'https://horo.mail.ru/prediction/',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "YaBrowser";v="24.7", "Yowser";v="2.5"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': ua.random,
    }

    # async web-request
    async with httpx.AsyncClient() as client:
        url = f'https://horo.mail.ru/prediction/{zodiac_en}/today/'
        response = await client.get(
            url=url,
            headers=headers
        )

    # parsing response with BeautifulSoup
    soup = await asyncio.to_thread(BeautifulSoup, response.text, 'html.parser')
    main_content = soup.find('main', itemprop='articleBody')

    # extraction text from target element
    text_lines = main_content.get_text(
        separator='\n',
        strip=True
    ).splitlines()

    # creating paragraphs
    paragraphs = ''.join([f'<p>{line}</p>' async for line in async_get_lines(text_lines)])
    return paragraphs

async def get_all_signs():
    all_signs = await get_all_zodiac_signs()
    date_today = datetime.today().strftime('%Y-%m-%d')
    date = all_signs[0].last_updated
    if str(date_today) == str(date):
        return all_signs
    names_of_signs = [it.zodiac_en for it in all_signs]
    new_data = {name:await fetch_horoscope(name) for name in names_of_signs}
    for zodiac_sign, description in new_data.items():
        await add_description_to_horoscope_sign(
            zodiac_name=zodiac_sign,
            description=description
        )
    return await get_all_zodiac_signs()
