import os
import requests
import json

from crendentials import token_API, chanel

try:
    with open('forecasts.json', 'r') as file:
        forecasts = json.load(file)
except FileNotFoundError:
    print('Прогнозы уже опубликованы')
    exit()

for i in range(len(forecasts)):
    header = forecasts[i]['header']
    content = forecasts[i]['content']
    time = forecasts[i]['time']

    string = f"""
    {header}\n
    {content}\n
    Когда: {time}"""
    r = requests.get(f'https://api.telegram.org/bot{token_API}/sendMessage?chat_id=@{chanel}&text={string}')

os.remove('forecasts.json')
