import os

BAIKAL_DAILY_ID = 1
IRK_RU_ID = 2
CITY_N_ID = 3

BAIKAL_DAILY_URL = "https://www.baikal-daily.ru"
IRK_RU_URL = "https://www.irk.ru/news/"
CITY_N_URL = "https://www.city-n.ru"


FILE_NAME = 'index.html'

BAIKAL_DAILY_FOLDER_PATH = os.path.join('parsing', 'BaikalDaily')
BAIKAL_DAILY_FILE_PATH = os.path.join(BAIKAL_DAILY_FOLDER_PATH, FILE_NAME)

IRK_RU_FOLDER_PATH = os.path.join('parsing', 'IrkRu')
IRK_RU_FILE_PATH = os.path.join(IRK_RU_FOLDER_PATH, FILE_NAME)

CITY_N_FOLDER_PATH = os.path.join('parsing', 'CityN')
CITY_N_FILE_PATH = os.path.join(CITY_N_FOLDER_PATH, FILE_NAME)


AGENCIES_IDS = [BAIKAL_DAILY_ID, IRK_RU_ID, CITY_N_ID]
