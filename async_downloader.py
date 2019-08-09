
import aiohttp
import asyncio
import requests


from phone_finder import PhoneFinder

list_urls = [
        'https://repetitors.info/',
        'https://hands.ru/company/about/',
        'http://сакмарскийрайон.рф/',
        'http://сакмарскийрайон.рф/Pages.aspx?id=36',
        'http://сакмарскийрайон.рф/Pages.aspx?id=535',
        'http://www.uralakva.ru/index.php?a=iv&id=4&pg_id=4'
    ] * 20



def init_phone_finder():
    param = {
            'len_local_phone': 6,
            'local_code': '3532',
            'len_international_phone': 11,
            'international_code': "8",
        }
    return PhoneFinder(**param)


async def fetch(url, session):
    async with session.get(url, timeout=30) as response:
        if response.status == 200:
            return url, await response.text()
        else:
            return url, None
            

async def get_phones(urls):
    phones = {}
    async with aiohttp.ClientSession() as session:
        pf = init_phone_finder()
        
        futures = []
        while urls:
            futures.append(fetch(urls.pop(), session))
        for future in asyncio.as_completed(futures):
            try:
                url, content = await future
            except:
                pass
            else:
                if content:
                    phones[url] = pf.get_phones(content)
                else:
                    phones[url] = None
    return phones


def async_download(urls):
    return asyncio.run(get_phones(urls))    


if __name__ == "__main__":
    print(async_download(list_urls))
    
    
