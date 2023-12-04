from requests import get
from bs4 import BeautifulSoup
from os import mkdir


def load_page(link):
    print('Loading', repr(link))
    while True:
        try:
            return get(link, timeout=5).text
        except BaseException as e:
            print(repr(e))


def read_article(link):
    while True:
        try:
            html = load_page(link)
            html = html[html.index('<div class="newsText">'):
                        html.index('<div class="afterNewItemMobileBanner mobileBanner" style="display:none;">')]
            text = BeautifulSoup(html, features='html.parser').get_text().strip()
            text = '\n'.join(' '.join(line.split()) for line in text.split('\n') if not line.startswith('Читайте також: '))
            return text
        except BaseException as e:
            print(repr(e))


NEED_LINKS = 10
INF = 10**9
try:
    mkdir('categories')
except FileExistsError:
    pass
for category in ['polytics', 'economy', 'society', 'culture', 'sports', 'technology', 'world', 'health', 'ato', 'vidbudova']:
    articles = set()
    for page in range(1, INF):
        before = len(articles)
        html = load_page(f'https://www.ukrinform.ua/rubric-{category}/block-lastnews?page={page}')
        for part in html.split(f'<a href="/rubric-{category}/')[1:]:
            part = part[: part.index('"')]
            link = f'https://www.ukrinform.ua/rubric-{category}/' + part
            file = 'categories/' + category + '/' + part[: -5] + '.txt'
            articles.add((link, file))
            if len(articles) == NEED_LINKS:
                break
        if len(articles) == NEED_LINKS or len(articles) == before:
            break
        print('found', len(articles), 'articles')
    try:
        mkdir('categories/' + category)
    except FileExistsError:
        pass
    for link, file in articles:
        open(file, 'w', encoding='utf-8').write(read_article(link))
