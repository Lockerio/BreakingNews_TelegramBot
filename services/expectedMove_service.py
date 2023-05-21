from serializers.expectedMove_serializer import ExpectedMoveSerializer


class ExpectedMoveService:
    def __init__(self, serializer: ExpectedMoveSerializer):
        self.serializer = serializer

    def get_one(self, expected_move_id):
        return self.serializer.get_one(expected_move_id)

    def get_one_by_user_id(self, user_id):
        return self.serializer.get_one_by_user_id(user_id)

    def get_all(self):
        return self.serializer.get_all()

    def update(self, data):
        user_id = data.get("user_id")
        expected_move = self.get_one_by_user_id(user_id)

        is_waiting_n = data.get("is_waiting_n")
        if is_waiting_n:
            expected_move.is_waiting_n = is_waiting_n

        amount_of_read_news = data.get("amount_of_read_news")
        if amount_of_read_news:
            expected_move.amount_of_read_news = amount_of_read_news

        return self.serializer.update(expected_move)

    def create(self, data):
        return self.serializer.create(data)

    def delete(self, agency_id):
        self.serializer.delete(agency_id)