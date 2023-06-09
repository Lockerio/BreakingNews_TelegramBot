import json

from container import userService, actionService, expectedMoveService, newsService, agencyService, favoritesService
from fill_db import fill_db_news
from parsing.BaikalDaily.baikal_daily import BaikalDailyParser
from parsing.CityN.city_n import CityNParser
from parsing.IrkRu.irk_ru import IrkRuParser
from parsing.meta import BAIKAL_DAILY_URL, CITY_N_URL, AGENCIES_IDS, IRK_RU_URL, BAIKAL_DAILY_FILE_PATH, \
    IRK_RU_FILE_PATH, CITY_N_FILE_PATH


class RequestHelper:
    def create_user(self, telegram_id: int, chat_id):
        """
        Создать пользователя.
        :param telegram_id: Телеграм id.
        :param chat_id: Чат id.
        :return: Id пользователя
        """
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
        """
        Найти и вернуть пользователя.
        :param telegram_id: Телеграм id.
        :return: Пользователь.
        """
        user = userService.get_one_by_telegram_id(telegram_id)
        if user:
            return user
        return None

    @staticmethod
    def record_user_actions(user_id, action):
        """
        Записать действия пользователя.
        :param user_id: Id пользователя.
        :param action: Действие, сделанное пользователем.
        """
        json_description = json.dumps(action)

        action_mapping = {
            "json_description": json_description,
            "user_id": user_id
        }
        actionService.create(action_mapping)

    @staticmethod
    def assert_save_n(user_id, n):
        """
        Сохранить количество новостей для просмотра.
        :param user_id: Id пользователя.
        :param n: Количество новостей для просмотра.
        :return: (True, подтверждение) - успешно сохранено, (False, текс ошибки) - возникла ошибка.
        """
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
        """
        Сохранить источник по умолчанию.
        :param telegram_id: Телеграм id.
        :param n: Количество новостей для просмотра.
        """
        user = self.get_user(telegram_id)
        mapping = {
            "user_id": user.id,
            "source_agency_id": int(n)
        }
        userService.update(mapping)

    @staticmethod
    def background_request():
        """
        Фоновая функция.
        :return:
        """
        try:
            baikalDailyParser = BaikalDailyParser(BAIKAL_DAILY_URL)
            baikalDailyParser.save_index_html_to_file(BAIKAL_DAILY_FILE_PATH, mode="w")
        except Exception as e:
            print(e)

        try:
            irkRuParser = IrkRuParser(IRK_RU_URL)
            irkRuParser.save_index_html_to_file(IRK_RU_FILE_PATH, mode="wb")
        except Exception as e:
            print(e)

        try:
            cityNParser = CityNParser(CITY_N_URL)
            cityNParser.save_index_html_to_file(CITY_N_FILE_PATH, mode="w")
        except Exception as e:
            print(e)

        is_there_newest_news = fill_db_news()

        return is_there_newest_news

    @staticmethod
    def get_sorted_chat_ids_by_user_favorites():
        """
        Найти чаты с подписками.
        :return: Чаты, пользователь которых подписан на какое-либо агентство.
        """
        all_chat_ids = {}
        for agency_id in AGENCIES_IDS:
            agencies_users = favoritesService.get_all_by_agency_id(agency_id)

            chat_ids = [
                userService.get_one(agency_user.user_id).chat_id
                for agency_user in agencies_users
            ]

            all_chat_ids[agency_id] = chat_ids

        return all_chat_ids

    @staticmethod
    def get_news(agency_id):
        return newsService.get_newest_agency_news(agency_id)

    @staticmethod
    def get_amount_of_read_news(user_id):
        return expectedMoveService.get_one_by_user_id(user_id).amount_of_read_news

    def get_news_desc(self, user):
        amount_of_read_news = self.get_amount_of_read_news(user.id)
        return newsService.get_special_news(user.source_agency_id,
                                            amount_of_read_news)

    @staticmethod
    def get_agencies():
        return agencyService.get_all()

    @staticmethod
    def get_agency(agency_id):
        return agencyService.get_one(agency_id)

    @staticmethod
    def assert_create_subscription(user_id, agency_id):
        """
        Создать подписку.
        :param user_id: Id пользователя.
        :param agency_id: Id агентства.
        :return: True - подписка создана, False - подписка уже существует.
        """
        mapping = {
            "user_id": user_id,
            "agency_id": agency_id
        }
        if favoritesService.create(mapping):
            return False
        return True

    @staticmethod
    def delete_favorite(user_id, agency_id):
        favoritesService.delete(user_id, agency_id)
