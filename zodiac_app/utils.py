import asyncio
import time
import httpx
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


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
    async with httpx.AsyncClient(timeout=300) as client:
        url = f'https://horo.mail.ru/prediction/{zodiac_en}/today/'
        while True:
            response = await client.get(url=url, headers=headers)
            if response.status_code == 200:
                break
            headers['user-agent'] = ua.random
            time.sleep(5)
    # parsing response with BeautifulSoup
    try:
        soup = await asyncio.to_thread(BeautifulSoup, response.text, 'html.parser')
    finally:
        while (main_content := soup.find('main', itemprop='articleBody')) is None:
            # to avoid race conditions
            time.sleep(3)

    # extraction text from target element
    text_lines = main_content.get_text(
        separator='\n',
        strip=True
    ).splitlines()

    # creating paragraphs
    paragraphs = ''.join([f'<p>{line}</p>' async for line in async_get_lines(text_lines)])
    return paragraphs
