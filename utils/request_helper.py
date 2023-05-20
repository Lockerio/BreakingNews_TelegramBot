import json

from container import userService, actionService, expectedMoveService
from fill_db import fill_db_news
from parsing.BaikalDaily.baikal_daily import BaikalDailyParser
from parsing.CityN.city_n import CityNParser
from parsing.IrkRu.irk_ru import IrkRuParser
from parsing.meta import IRK_RU_URL, BAIKAL_DAILY_URL, CITY_N_URL



class RequestHelper:
    def create_user(self, telegram_id: int, chat_id):
        user_id = self.get_user_id(telegram_id)
        if not user_id:
            user_mapping = {
                "telegram_id": telegram_id,
                "chat_id": chat_id
            }
            user = userService.assert_news_create(user_mapping)
            expectedMoveService.assert_news_create({"user_id": user.id})
            return user.id
        return user_id

    @staticmethod
    def get_user_id(telegram_id: int):
        user = userService.get_one_by_telegram_id(telegram_id)
        if user:
            return user.id
        return None

    @staticmethod
    def record_user_actions(user_id, action):
        json_description = json.dumps(action)

        action_mapping = {
            "json_description": json_description,
            "user_id": user_id
        }
        actionService.assert_news_create(action_mapping)

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

    @staticmethod
    def background_request():
        while True:
            # Filling db with the newest news
            baikalDailyParser = BaikalDailyParser(BAIKAL_DAILY_URL)
            baikalDailyParser.save_index_html_to_file()

            irkRuParser = IrkRuParser(IRK_RU_URL)
            irkRuParser.save_index_html_to_file()

            cityNParser = CityNParser(CITY_N_URL)
            cityNParser.save_index_html_to_file()

            is_there_newest_news = fill_db_news()

            return is_there_newest_news
