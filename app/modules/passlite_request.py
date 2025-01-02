import requests
import urllib.parse
from dotenv import load_dotenv
import os
load_dotenv('.env')
cookies = {
    "_ym_uid": os.getenv("_ym_uid"),
    "_ym_d": os.getenv("_ym_d"),
    "_ym_isad": os.getenv("_ym_isad"),
    "PHPSESSID": os.getenv("PHPSESSID")
}
def passlite_request(name, date):
    form_data = {
        "passType": "single",
        "requestName": "ГАБ ПРОДУКТ",
        "requestType": "person",
        "carNumber": "",
        "carType": "",
        "personInfo": name,
        "requestDate": date,
        "requestDateStart": "",
        "requestDateEnd": ""
    }
    encoded_params = urllib.parse.urlencode(form_data)
    r = requests.post('https://passlite.ru/lk/requestAdd.php', cookies=cookies, data=form_data)
    return r.json()
