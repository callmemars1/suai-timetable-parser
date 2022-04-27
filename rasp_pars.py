from bs4 import BeautifulSoup as bs
import requests
import json
import re

group_table = []
TABLE_PATH = 'table.json'

REQ_URL = 'http://rasp.guap.ru/'

req = requests.get(REQ_URL)
soup = bs(req.text, "html.parser")

combobox_info = soup.find('div', class_='form').find('select').find_all('option')

regexp = r'(\d+)(..)((\d+|[а-яА-Я]+)(\d*|[а-яА-Я]*)([а-яА-Я]*))'

for value in combobox_info:
    match = (re.search(regexp, str(value)))
    if match is not None:
        page_number = int(match.group(1))
        group = str(match.group(3))
        group_table.append(
            {'page_number': page_number,
             'group': group}
        )

with open(TABLE_PATH, 'w') as file:
    json.dump(group_table, file, indent=2, ensure_ascii=False)
