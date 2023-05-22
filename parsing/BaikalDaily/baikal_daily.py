from bs4 import BeautifulSoup

from parsing.parser_parent import ParserParent
from parsing.meta import BAIKAL_DAILY_URL, BAIKAL_DAILY_ID


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
                    "news_agency_id": BAIKAL_DAILY_ID
                }
                to_save.append(news_data)
            news = news.find_next_sibling()
        return to_save


if __name__ == '__main__':
    pass
