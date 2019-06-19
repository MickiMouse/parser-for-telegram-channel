import json
import requests

from bs4 import BeautifulSoup
from crendentials import BASE_URL

session = requests.Session()


def get_html(url):
    response = session.get(url)
    if response.status_code == 200:
        print('Status OK!')
        return response.content
    print('404')
    return ''


def parse(content):
    soup = BeautifulSoup(content, 'lxml')

    """Parse all cards"""
    div = soup.find('div', attrs={'class': 'row forecasts-row'})
    cards = div.find_all('div', attrs={'class': 'col-md-4'})

    """Parse links of all cards"""
    links = [c.find('a', attrs={'class': 'article-card forecast-card'}).get('href') for c in cards]
    print(f'Links : {len(links)}')

    """Parse time of all cards"""
    times = [
        t.find(
            name='footer',
            attrs={'class': 'footer'}
        ).findChild(
            name='div',
            attrs={'class': 'forecast-result'},
            recursive=False).get('title')
        for t in cards
    ]
    data = []
    for i in range(len(links)):
        response = session.get(BASE_URL + links[i])
        soup = BeautifulSoup(response.content, 'lxml')

        """Parse header"""
        h1 = soup.find('h1', attrs={'class': 'heading heading-1'}).text

        """Parse content"""
        content = soup.find('div', attrs={'class': 'content-body'})
        full_text = content.findChildren('p', recursive=False)
        text_list = [p.text.strip() for p in full_text]
        text_str = ' '.join(text_list)

        data.append({'header': h1, 'content': text_str, 'time': times[i]})
        print(f'Have done {i+1} : {len(links)}')

    return data


def main(url, filename):
    r = get_html(url)
    forecasts = parse(r)

    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(forecasts, file, indent=4)

    print('Save JSON')
    return 1


main(BASE_URL + '/tips/tomorrow', 'forecasts.json')
