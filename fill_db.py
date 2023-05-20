import os

from container import agencyService
from parsing.BaikalDaily.baikal_daily import BaikalDailyParser
from parsing.urls import BAIKAL_DAILY_URL


def fill_db():
    agencies = [
        {
            "name": "Байкал Daily",
            "description": "Новости Бурятии и Улан-Удэ в реальном времени.",
            "beauty_url": "baikal-daily.ru"
        },
        {
            "name": "IRK.RU",
            "description": "Новости Иркутска.",
            "beauty_url": "irk.ru"
        },
        {
            "name": "Norilsk city",
            "description": "ОФИЦИАЛЬНЫЙ САЙТ ГОРОДА НОРИЛЬСКА.",
            "beauty_url": "norilsk-city.ru"
        },
    ]

    for agency in agencies:
        agencyService.create(agency)


if __name__ == '__main__':
    fill_db()

    current_dir = os.getcwd()
    folder_path = os.path.join(current_dir, 'parsing', 'BaikalDaily')
    file_path = os.path.join(folder_path, 'index.html')

    baikalDailyParser = BaikalDailyParser(BAIKAL_DAILY_URL)
    news = baikalDailyParser.find_news(file_path)
    baikalDailyParser.save_news_to_db(news)
