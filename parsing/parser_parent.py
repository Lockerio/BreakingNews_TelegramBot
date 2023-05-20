import requests

from config import HEADERS
from container import newsService


class ParserParent:
    def __init__(self, url):
        self.url = url
        self.headers = HEADERS

    def save_index_html_to_file(self):
        req = requests.get(self.url, headers=self.headers)
        src = req.text

        with open("index.html", "w") as file:
            file.write(src)

    def find_news(self, file):
        pass

    @staticmethod
    def save_news_to_db(news):
        for item in news:
            newsService.create(item)


if __name__ == '__main__':
    pass
