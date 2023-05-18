import json

from container import userService, actionService


class RequestHelper:
    def create_user(self, telegram_id: int):
        user_id = self.get_user_id(telegram_id)
        if not user_id:
            user_mapping = {
                "telegram_id": telegram_id
            }
            user = userService.create(user_mapping)
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
