from bs4 import BeautifulSoup

from parsing.parser_parent import ParserParent
from parsing.urls import BAIKAL_DAILY_URL


class BaikalDailyParser(ParserParent):
    def __init__(self, url):
        super().__init__(url)

    def find_news(self, file):
        with open(file, "r") as file:
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
                    "url": self.url + item.get("href"),
                    "news_agency_id": 1
                }
                to_save.append(news_data)
            news = news.find_next_sibling()
        return to_save


if __name__ == '__main__':
    baikalDailyParser = BaikalDailyParser(BAIKAL_DAILY_URL)
    baikalDailyParser.save_index_html_to_file()
