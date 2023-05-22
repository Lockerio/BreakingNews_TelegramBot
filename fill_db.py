import os

from container import agencyService
from parsing.BaikalDaily.baikal_daily import BaikalDailyParser
from parsing.CityN.city_n import CityNParser
from parsing.IrkRu.irk_ru import IrkRuParser
from parsing.meta import BAIKAL_DAILY_URL, IRK_RU_URL, CITY_N_URL, BAIKAL_DAILY_ID, IRK_RU_ID, CITY_N_ID, \
    BAIKAL_DAILY_FILE_PATH, IRK_RU_FILE_PATH, CITY_N_FILE_PATH


def fill_db_agencies():
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
            "name": "City-n",
            "description": "Новости Кемеровской области.",
            "beauty_url": "city-n.ru"
        },
    ]

    for agency in agencies:
        agencyService.create(agency)


def fill_db_news():
    is_there_newest_news = {}

    # BaikalDaily
    baikalDailyParser = BaikalDailyParser(BAIKAL_DAILY_URL)
    news = baikalDailyParser.find_news(BAIKAL_DAILY_FILE_PATH)
    is_there_newest_news[BAIKAL_DAILY_ID] = baikalDailyParser.assert_save_news_to_db(news)

    # IrkRu
    irkRuParser = IrkRuParser(IRK_RU_URL)
    news = irkRuParser.find_news(IRK_RU_FILE_PATH)
    is_there_newest_news[IRK_RU_ID] = irkRuParser.assert_save_news_to_db(news)

    # CityN
    cityNParser = CityNParser(CITY_N_URL)
    news = cityNParser.find_news(CITY_N_FILE_PATH)
    is_there_newest_news[CITY_N_ID] = cityNParser.assert_save_news_to_db(news)

    return is_there_newest_news


if __name__ == '__main__':
    fill_db_agencies()
    fill_db_news()
