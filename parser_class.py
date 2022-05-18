from bs4 import BeautifulSoup as bs
import requests


class Parser:

    def __init__(self, url):
        self.url = url
        self.request = self.get_request()
        self.soup = bs(self.request.text, "html.parser")

    def get_request(self):
        try:
            request = requests.get(self.url)
            if request.status_code == 200:
                return request
        except:
            print("Connection error")
