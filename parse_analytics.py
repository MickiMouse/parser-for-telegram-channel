import json
import requests

from bs4 import BeautifulSoup
from credentials import BASE_URL, PATH

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

        data.append(
            {
                'header': h1,
                'content': text_str,
                'time': times[i]
            }
        )
        print(f'Have done {i+1} : {len(links)}')
    return data


def main(url, filename='forecasts.json'):
    r = get_html(url)
    forecasts = parse(r)

    with open(PATH + filename, 'r', encoding='utf-8') as file:
        data = json.load(file)

    data_headers = set([data[i]['header'] for i in range(len(data))])
    fore_headers = set([forecasts[i]['header'] for i in range(len(forecasts))])

    filterheaders = fore_headers.difference(data_headers)
    filterforecasts = [forecast for forecast in forecasts if forecast['header'] in filterheaders]

    with open(PATH + filename, 'w', encoding='utf-8') as file:
        json.dump(filterforecasts, file, indent=4, ensure_ascii=False)

    print('Save JSON')
    return 1


if __name__ == '__main__':
    main(BASE_URL + '/tips/tomorrow')
