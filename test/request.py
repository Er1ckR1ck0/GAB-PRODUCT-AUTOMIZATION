import requests
import json
# action = 'get-record'  # указываем действие (метод)
# rk = '41f1ad343f5b08ad96ac064130c45e9a8b871b1560dd36692ce8d462b2e5e2c6'  # указываем ключ

# # получаем запись
# query_data = {'id': 4990400 , 'rk': rk}

# query_url = f'https://rubitime.ru/api2/{action}'

# response = requests.post(query_url, json=query_data)

# if response.ok:
#     result = response.json()
#     if result['status'] == 'ok':
#         print(f"Success: {result['message']}")  # сообщение о успешном запросе
#         print(result['data'])  # полученные данные
#     else:
#         print(f"Error: {result['message']}")  # сообщение об ошибке при выполнении запроса
# else:
#     print("Empty response")  # запрос не вернул никакого результата

data = {'id': 4990400, 'parent_record': None, 'whom': 0, 'created_at': '2024-09-15 08:02:20', 'updated_at': '2024-09-15 13:00:08', 'record': '2024-09-16 13:00:00', 'name': 'Чардымская Анна Андреевна', 'price': '2400', 'phone': '+79641851460', 'email': 'hello.iamegor@yandex.ru', 'comment': '', 'status': 0, 'status_title': 'Записан', 'cooperator_id': 25261, 'cooperator_title': 'MINI (м.Озёрная)', 'branch_id': 12313, 'branch_title': 'Студия звукозаписи (gãb.sound)', 'service_id': 39420, 'service_title': 'Почасово "ДНЕВНОЕ"', 'url': 'https://gabsound.rubitime.ru/widget/card/4bba1a9cdffb833469ff2253763a9ccf6ea9dfa3e1c59a8b77ee1e2b92f47dd3', 'coupon': None, 'coupon_discount': None, 'source': None, 'cancelReason': None, 'duration': '240', 'prepayment': '2400', 'prepayment_date': '2024-09-15 08:04:09', 'prepayment_url': 'https://gabsound.rubitime.ru/widget/prp/7499040066e66a6224a4f186', 'reminder': '2024-09-15 13:00:00', 'custom_field1': '2', 'custom_field2': '', 'custom_field3': 'Telegram', 'custom_field4': 'timo_sv', 'custom_field5': '', 'custom_field6': 'Нет', 'custom_field7': None, 'custom_field8': None, 'custom_field9': None, 'custom_field10': None, 'custom_field11': None, 'custom_field12': None, 'custom_field13': None, 'custom_field14': None, 'custom_field15': None, 'custom_field16': None, 'custom_field17': None, 'custom_field18': None, 'custom_field19': None, 'custom_field20': None}
data = json.dumps(data)
print(data)
requests.post('http://127.0.0.7:8000/api/gateway/', json=data)