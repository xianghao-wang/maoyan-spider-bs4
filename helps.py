import requests
import os
import json
from bs4 import BeautifulSoup

def get_one_page(url):
    """
        爬取具体一页 sample: url=https://maoyan.com/board/4?offset=0
        @param url: 要抓取页面的url
        @return: 网页的html文本
    """

    headers = {
        'User-Agent': os.getenv('USER_AGENT'),
        'Cookie': os.getenv('COOKIE')
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.text
    else:
        return None

def parse_one_page(text):
    """
        解析html文本
        @param text: 要被解析的html文本
        @return: generator[{
            'index', 'image', 'title', 'actor', 'time', 'score'
        }]
    """

    soup = BeautifulSoup(text, 'lxml')
    dds = soup.find_all(name='dd')
    for dd in dds:
        index = dd.i.string.strip()
        image = dd.a.img.find_next_sibling()['data-src'].strip()
        title = dd.find(name='p', class_='name').find(name='a').string.strip()
        actor = dd.find(name='p', class_='star').string.strip()
        time = dd.find(name='p', class_='releasetime').string.strip()
        integer = dd.find(name='i', class_='integer').string.strip()
        fraction = dd.find(name='i', class_='fraction').string.strip()

        yield {
            'index': index,
            'image': image,
            'title': title,
            'actor': actor[3:] if len(actor) > 3 else '',
            'time': time[5:] if len(time) > 5 else '',
            'score': integer + fraction
        }
    

def write_to_file(content):
    with open(os.getenv('RESULT_FILE'), 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')