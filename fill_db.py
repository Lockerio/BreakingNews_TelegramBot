import os

from container import agencyService
from parsing.BaikalDaily.baikal_daily import BaikalDailyParser
from parsing.CityN.city_n import CityNParser
from parsing.IrkRu.irk_ru import IrkRuParser
from parsing.meta import BAIKAL_DAILY_URL, IRK_RU_URL, CITY_N_URL


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
        agencyService.assert_news_create(agency)


def fill_db_news():
    is_there_newest_news = {}
    current_dir = os.getcwd()

    # BaikalDaily
    baikal_daily_folder_path = os.path.join(current_dir, 'parsing', 'BaikalDaily')
    baikal_daily_file_path = os.path.join(baikal_daily_folder_path, 'index.html')

    baikalDailyParser = BaikalDailyParser(BAIKAL_DAILY_URL)
    news = baikalDailyParser.find_news(baikal_daily_file_path)
    is_there_newest_news['BaikalDaily'] = baikalDailyParser.assert_save_news_to_db(news)

    # IrkRu
    irk_ru_folder_path = os.path.join(current_dir, 'parsing', 'IrkRu')
    irk_ru_file_path = os.path.join(irk_ru_folder_path, 'index.html')

    irkRuParser = IrkRuParser(IRK_RU_URL)
    news = irkRuParser.find_news(irk_ru_file_path)
    is_there_newest_news['IrkRu'] = irkRuParser.assert_save_news_to_db(news)

    # CityN
    city_n_folder_path = os.path.join(current_dir, 'parsing', 'CityN')
    city_n_file_path = os.path.join(city_n_folder_path, 'index.html')

    cityNParser = CityNParser(CITY_N_URL)
    news = cityNParser.find_news(city_n_file_path)
    is_there_newest_news['CityN'] = cityNParser.assert_save_news_to_db(news)

    return is_there_newest_news


if __name__ == '__main__':
    fill_db_agencies()
    fill_db_news()
