from bs4 import BeautifulSoup

from parsing.parser_parent import ParserParent
from parsing.meta import CITY_N_URL, CITY_N_ID


class CityNParser(ParserParent):
    def __init__(self, url):
        super().__init__(url)

    def find_news(self, file):
        with open(file, "r") as file:
            src = file.read()

        soup = BeautifulSoup(src, "lxml")
        news = soup.find("div", {"class": "hot_news local_news"})
        to_save = []

        while news:
            item = news.find("div", {"class": "news_title"})
            text = news.find("div", {"class": "news_lide"})
            if item and text:
                news_data = {
                    "title": item.find("p").text.strip(),
                    "text": text.find("span").text,
                    "url": self.url + item.find("a").get("href"),
                    "news_agency_id": CITY_N_ID
                }
                to_save.append(news_data)
            news = news.find_next_sibling()
        return to_save


if __name__ == '__main__':
    pass
