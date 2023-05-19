import requests
from bs4 import BeautifulSoup

from config import HEADERS


class BaikalDailyParser:
    def __init__(self):
        self.url = "https://www.baikal-daily.ru"
        self.headers = HEADERS

    def save_index_html_to_file(self):
        req = requests.get(self.url, headers=self.headers)
        src = req.text

        with open("index.html", "w") as file:
            file.write(src)

    def find_news(self):
        with open("index.html", "r") as file:
            src = file.read()

        soup = BeautifulSoup(src, "lxml")
        news = soup.find("div", {"id": "front_news_main_center"}).find("div", {"class": "news-item"})
        to_save = []

        while news:
            item = news.find("a")
            if item:
                news_data = {
                    "title": item.text.strip(),
                    "text": news.find("div", {"class": "news-preview-text"}).text.strip(),
                    "url": self.url + item.get("href")
                }
                to_save.append(news_data)
            news = news.find_next_sibling()
        return to_save

    @staticmethod
    def save_news_to_db(news):
        pass


if __name__ == '__main__':
    baikalDailyParser = BaikalDailyParser()
    # baikalDailyParser.save_index_html_to_file()

    news = baikalDailyParser.find_news()

