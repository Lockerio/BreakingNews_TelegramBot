import json

from container import userService, actionService, expectedMoveService


class RequestHelper:
    def create_user(self, telegram_id: int):
        user_id = self.get_user_id(telegram_id)
        if not user_id:
            user_mapping = {
                "telegram_id": telegram_id
            }
            user = userService.create(user_mapping)
            a = expectedMoveService.create({"user_id": user.id})
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
        actionService.create(action_mapping)

    @staticmethod
    def assert_save_n(user_id, n):
        action_mapping = {
            "user_id": user_id,
            "news_amount_to_show": n
        }
        try:
            userService.update_news_amount_to_show(action_mapping)

        except ValueError as e:
            error_message = str(e)
            return False, error_message

        except Exception as e:
            error_message = str(e)
            return False, error_message



        message = f"Количество новостей для показа изменено на <b>{n}</b>"
        return True, message
