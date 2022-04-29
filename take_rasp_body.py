from bs4 import BeautifulSoup as bs
import requests
import json
import re

group_table = []
TABLE_PATH = 'table.json'

REQ_URL = 'https://rasp.guap.ru/?g=315'

req = requests.get(REQ_URL)
soup = bs(req.text, "html.parser")

# combobox_info = soup.find('div', class_='form').find('select').find_all('option')
class_result = soup.find('div', class_='result')

day = class_result.find_all('h3')
lesson_number = class_result.find_all('h4')
class_study = class_result.find_all('div', class_='study')
chota = class_result.find('h3').find_next_sibling('h4').find_next_sibling().find_next()

#
# h3_tags = class_result.find_all('h3')
# for index, h3 in enumerate(h3_tags):
#     print("---------------------------------------------------------")
#     print(h3_tags[index])
#     while h3.find_next_sibling() != h3_tags[index + 1]:
#         nex_el = h3.find_next_sibling()
#         h3 = nex_el
#         print(nex_el)
#
#         ###
#
#
# # print(day)
# # print(lesson_number)
# # print(class_study)
# # print(chota)
