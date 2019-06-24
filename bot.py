import requests
import json
import datetime
from credentials import channel, PATH, URL


def send_message(chat_id, _text):
    message = {'chat_id': chat_id, 'text': _text}
    response = requests.post(URL + '/sendMessage', json=message)
    return response.json()


with open(PATH + 'forecasts.json', 'r') as file:
    forecasts = json.load(file)

if len(forecasts) == 0:
    text = 'Прогнозы уже опубликованы'
    now = datetime.datetime.now()
    print(f'{text}, {now}')
    exit()

for i in range(len(forecasts)):
    header = forecasts[i]['header']
    content = forecasts[i]['content']
    time = forecasts[i]['time']

    text = f"""{header}\n{content}\nКогда: {time}"""
    send_message(f'@{channel}', text)
