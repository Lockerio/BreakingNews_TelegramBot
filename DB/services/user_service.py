from DB.serializers.user_serializer import UserSerializer


class UserService:
    def __init__(self, serializer: UserSerializer):
        self.serializer = serializer

    def get_one(self, user_id):
        return self.serializer.get_one(user_id)

    def get_all(self):
        return self.serializer.get_all()

    def create(self, data):
        return self.serializer.create(data)

    def update_news_amount_to_show(self, data):
        user_id = data.get("id")
        user = self.get_one(user_id)

        n = data.get("news_amount_to_show")

        if not (0 < n < 10):
            raise ValueError("Ошибка! Вы можете получать от 0 до 10 постов за раз")

        user.news_amount_to_show = n
        return self.serializer.update_news_amount_to_show(user)

    def delete(self, user_id):
        self.serializer.delete(user_id)
