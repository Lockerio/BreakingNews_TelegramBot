from serializers.user_serializer import UserSerializer


class UserService:
    def __init__(self, serializer: UserSerializer):
        self.serializer = serializer

    def get_one(self, user_id):
        return self.serializer.get_one(user_id)

    def get_one_by_telegram_id(self, telegram_id):
        return self.serializer.get_one_by_telegram_id(telegram_id)

    def get_all(self):
        return self.serializer.get_all()

    def get_chat_ids_from_user_with_definite_source_agency(self, source_agency_id):
        users = self.serializer.get_user_by_source_agency_id(source_agency_id)
        chat_ids = [user.chat_id for user in users]
        return chat_ids

    def create(self, data):
        return self.serializer.create(data)

    def update(self, data):
        user_id = data.get("user_id")
        user = self.get_one(user_id)

        new_n = data.get("news_amount_to_show")
        if new_n:
            try:
                n = int(new_n)

            except Exception:
                raise Exception("Ошибка! Вы отправляете не число🤕")

            if not (0 < n < 11):
                raise ValueError("Ошибка! Вы можете получать от 1 до 10 постов за раз.")
            user.news_amount_to_show = n

        new_source_id = data.get("source_agency_id")
        if new_source_id:
            user.source_agency_id = new_source_id

        return self.serializer.update(user)

    def delete(self, user_id):
        self.serializer.delete(user_id)
