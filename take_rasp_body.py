from bs4 import BeautifulSoup as bs
import requests
import logging
import json
import re

TEST_URL = 'https://rasp.guap.ru/?g=315'


class RaspBodyParser:
    def __init__(self, url):
        self.url = url
        self.request = self.get_request()
        self.soup = bs(self.request.text, "html.parser")
        self.class_result = self.soup.find('div', class_='result')

    def get_request(self):
        try:
            request = requests.get(self.url)
            if request.status_code == 200:
                return request
        except:
            print("Connection error")

    def divide_by_days(self):
        days = []

        h3_tags = self.class_result.find_all('h3')
        for index, h3 in enumerate(h3_tags):
            day = [h3_tags[index]]
            if index + 1 < len(h3_tags):
                while h3.find_next_sibling() != h3_tags[index + 1]:
                    nex_el = h3.find_next_sibling()
                    h3 = nex_el
                    day.append(nex_el)
            else:
                while h3.find_next_sibling() is not None:
                    nex_el = h3.find_next_sibling()
                    h3 = nex_el
                    day.append(nex_el)
            days.append(day)
        return days


rasp_5038 = RaspBodyParser(TEST_URL)

for day in rasp_5038.divide_by_days():
    print(day)
