import requests
import json

api_url = 'https://api.weatherbit.io/v2.0/forecast/daily'

params = {
    'city': 'Yaroslavl',
    'country': 'RU',
    'lang': 'eu',
    'days': 15,
    'key': '5ce1aed18f4f4260a4e564a1212bb059'
}

res = requests.get(api_url, params=params)
weather = res.json()

def send_weather(day):

    text = [] # испольлзовать лист
    text.append(str(weather['data'][day]['temp']))
    text.append(str(weather['data'][day]['valid_date']))
    return text

print(weather['data'][6]['wind_spd'])
print(weather['city_name'])

