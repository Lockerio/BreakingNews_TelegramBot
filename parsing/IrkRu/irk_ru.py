from bs4 import BeautifulSoup

from parsing.parser_parent import ParserParent
from parsing.meta import IRK_RU_URL, IRK_RU_ID


class IrkRuParser(ParserParent):
    def __init__(self, url):
        super().__init__(url)

    def find_news(self, file):
        with open(file, "r") as file:
            src = file.read()

        soup = BeautifulSoup(src, "lxml")
        news = soup.find("li", {"class": "b-news-article-list-item"})
        to_save = []

        while news:
            item = news.find("h2")
            if item:
                news_data = {
                    "title": item.text.strip(),
                    "text": news.find("p").text.strip(),
                    "url": self.url + news.find("a").get("href"),
                    "news_agency_id": IRK_RU_ID
                }
                to_save.append(news_data)
            news = news.find_next_sibling()

        return to_save


if __name__ == '__main__':
    irkRuParser = IrkRuParser(IRK_RU_URL)
    irkRuParser.save_index_html_to_file()
