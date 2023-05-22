import requests

from config import HEADERS
from container import newsService


class ParserParent:
    def __init__(self, url):
        self.url = url
        self.headers = HEADERS

    def save_index_html_to_file(self, file, mode):
        req = requests.get(self.url, headers=self.headers)
        src = req.text

        if mode == "wb":
            with open(file, "wb") as file:
                file.write(src.encode("utf-8"))

        elif mode == "w":
            with open(file, "w") as file:
                file.write(src)

    def find_news(self, file):
        pass

    @staticmethod
    def assert_save_news_to_db(news):
        is_there_newest_news = False
        for item in news[::-1]:
            if newsService.assert_news_create(item):
                is_there_newest_news = True

        return is_there_newest_news


if __name__ == '__main__':
    pass
