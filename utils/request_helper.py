import json

from container import userService, actionService, expectedMoveService, newsService, agencyService
from fill_db import fill_db_news
from parsing.BaikalDaily.baikal_daily import BaikalDailyParser
from parsing.CityN.city_n import CityNParser
from parsing.IrkRu.irk_ru import IrkRuParser
from parsing.meta import BAIKAL_DAILY_URL, CITY_N_URL, AGENCIES_IDS, IRK_RU_URL


class RequestHelper:
    def create_user(self, telegram_id: int, chat_id):
        user_id = self.get_user(telegram_id)
        if not user_id:
            user_mapping = {
                "telegram_id": telegram_id,
                "chat_id": chat_id
            }
            user = userService.create(user_mapping)
            expectedMoveService.create({"user_id": user.id})
            return user.id
        return user_id

    @staticmethod
    def get_user(telegram_id: int):
        user = userService.get_one_by_telegram_id(telegram_id)
        if user:
            return user
        return None

    @staticmethod
    def record_user_actions(user_id, action):
        json_description = json.dumps(action)

        action_mapping = {
            "json_description": json_description,
            "user_id": user_id
        }
        actionService.create(action_mapping)

    @staticmethod
    def assert_save_n(user_id, n):
        action_mapping = {
            "user_id": user_id,
            "news_amount_to_show": n
        }
        try:
            userService.update(action_mapping)

        except ValueError as e:
            error_message = str(e)
            return False, error_message

        except Exception as e:
            error_message = str(e)
            return False, error_message

        message = f"Количество новостей для показа изменено на <b>{n}</b>"
        return True, message

    def save_source(self, telegram_id, n):
        user = self.get_user(telegram_id)
        mapping = {
            "user_id": user.id,
            "source_agency_id": int(n)
        }
        userService.update(mapping)

    @staticmethod
    def background_request():
        baikalDailyParser = BaikalDailyParser(BAIKAL_DAILY_URL)
        baikalDailyParser.save_index_html_to_file()

        irkRuParser = IrkRuParser(IRK_RU_URL)
        irkRuParser.save_index_html_to_file()

        cityNParser = CityNParser(CITY_N_URL)
        cityNParser.save_index_html_to_file()

        is_there_newest_news = fill_db_news()
        print(is_there_newest_news)

        return is_there_newest_news

    @staticmethod
    def get_sorted_chat_ids_with_sources_agency_id():
        all_chat_ids = {}
        for agency_id in AGENCIES_IDS:
            chat_ids = userService.get_chat_ids_from_user_with_definite_source_agency(agency_id)
            all_chat_ids[agency_id] = chat_ids
        return all_chat_ids

    @staticmethod
    def get_news(agency_id):
        return newsService.get_newest_agency_news(agency_id)

    @staticmethod
    def get_agencies():
        return agencyService.get_all()
