# Получаем ID всех городов по вырытому с сайта списку регионов
import requests
from fake_useragent import UserAgent
import json

regions = [1, 4593, -1, 4553, 4554, 4555, 4556, 4557, 4558, 4560, 4561, 4562, 4563, 4564, 4565, 4566, 4567, 4568, 4569, 4570, 4571, 4572, 4573, 4574, 4575, 4576, 4577, 4578, 4579, 4580, 4581, 4582, 4583, 4584, 4585, 4586, 4587, 4588, 4589, 4590, 4591, 4592, 4594, 4595, 4596, 4597, 4598, 4599, 4600, 4601, 4602, 4603, 4604, 4605, 4606, 4607, 4608, 4609, 4610, 4611, 4612, 4613, 4614, 4615, 4617, 4618, 4619, 4620, 4621, 4622, 4623, 4624, 4625, 4627, 4628, 4629, 4630, 4631, 4633, 4635, 4636, 181462, 184723, 187450, 2, -2]

def fetch(url, json={}):
    try:
        res = requests.get(url, headers={'User-Agent': UserAgent().random}, json=json)
        print(res.status_code)
        return res.text
    except Exception as e:
        print(f'FETCH ERROR: {e}')
        return None

cities = []

for region in regions:
    res = fetch(f'https://vladivostok.cian.ru/cian-api/site/v1/get-region-cities/?regionId={region}')
    raw_cities = json.loads(res)
    print(raw_cities)

    for city in raw_cities['data']['items']:
        cities.append({
            'id': city['id'],
            'name': city['displayName']
        })

cities_file = open('cities.json', 'w', encoding='utf-8')
json.dump(cities, cities_file, indent=4, ensure_ascii=False)
print('success')