import requests
from bs4 import BeautifulSoup
import pandas as pd

base_url = 'https://quotes.toscrape.com'
search_query = input('Введите запрос: ')
response = requests.get(base_url)
if response.status_code == 200:
    soup1 = BeautifulSoup(response.content, 'html.parser')
    categories_box = soup1.find('div', class_="col-md-4 tags-box")
    categories_links = categories_box.find_all('a')
    target_url = None
    for link in categories_links:
        category = link.text.strip().lower()
        if search_query in category:
            target_url = base_url + link.get('href')
            print(f'Категория найдена {link.text.strip()}')
            break
    if target_url:
        response2 = requests.get(target_url)
        if response2.status_code == 200:
            soup2 = BeautifulSoup(response2.content, 'html.parser')
            cards = soup2.find_all('div', class_="quote")
            data=[]
            for card in cards:
                content_tag = card.find('span', class_='text')
                author_tag = card.find('small', class_='author')
                content = content_tag.text.strip()
                author = author_tag.text.strip()
                data.append({
                    'content': content,
                    'author': author
                })
            if data:
                df = pd.DataFrame(data, columns=['content', 'author'])
                df.to_excel('data.xlsx', index=False)
                print(f'Всё прошлое успешно. {len(data)} цитат добавлено')
            else:
                print('Ошибка')
        else:
            print('Ошибка в статус коде')
    else:
        print('такого нет')

