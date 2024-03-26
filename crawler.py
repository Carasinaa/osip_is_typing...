from bs4 import BeautifulSoup
import re
import requests
from fake_useragent import UserAgent
from tqdm.auto import tqdm
import pandas as pd

ua = UserAgent()
session = requests.session()

# функции для парсинга страницы со стихами и каждого стиха отдельно, потом функция run_all, которая проходится по всему сайту
def parse_news_page_block(one_block):
    block = {}
    p = one_block.find('a')
    block['href'] = p.attrs['href']
    title = p.text.split(' — ')[1]
    block['title'] = title
    return block


def parse_one_article(block):
    url_one = block['href']
    req = session.get(url_one, headers={'User-Agent': ua.random})
    page = req.text
    soup = BeautifulSoup(page, 'html.parser')
    verse = soup.find('div', {'class': 'entry-content poem-text'}).text
    verse = (verse.split('Анализ стихотворения'))[0]
    block['verse'] = verse
    return block


def get_page(page_number):
    url = f'https://rustih.ru/osip-mandelshtam/page/{page_number}/'
    req = session.get(url, headers={'User-Agent': ua.random})
    page = req.text
    soup = BeautifulSoup(page, 'html.parser')
    poetry = soup.find_all('div', {'class': 'post-card-one'})
    all_blocks = []
    result = []
    for p in poetry:
        b = parse_news_page_block(p)
        all_blocks.append(b)
        if b['href'].startswith('https://'):
            idx = all_blocks.index(b)
            try:
                res = parse_one_article(b)
                res['id'] = idx + 1
                result.append(res)
            except Exception as e:
                print(e)
    return result


def run_all(n_pages):
    all_blocks = []
    for i in tqdm(range(n_pages)):
        all_blocks.extend(get_page(i+1))

    return all_blocks


blocks = run_all(5)
df = pd.DataFrame(blocks)
df = df.drop_duplicates()

# сохраняем в датафрейм
df.to_csv('output.csv', encoding='utf-8')
