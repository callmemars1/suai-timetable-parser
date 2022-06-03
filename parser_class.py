from bs4 import BeautifulSoup as bs
import requests
from loguru import logger


class Parser:
    """Makes a request and creates a soup object"""
    def __init__(self, url):
        self.url = url
        self.request = self.get_request()
        self.soup = bs(self.request.text, "html.parser")

    def get_request(self):
        try:
            request = requests.get(self.url)
            if request.status_code == 200:
                return request
        except Exception as _ex:
            logger.warning(f"Connection error, cant  requests.get({self.url})", _ex)
