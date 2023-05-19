from container import expectedMoveService


class AnswerHelper:
    @staticmethod
    def is_user_waiting_n(user_id):
        return expectedMoveService.get_one_by_user_id(user_id).is_waiting_n

    @staticmethod
    def update_user_waiting_n(user_id, is_waiting_n):
        mapping = {
            "user_id": user_id,
            "is_waiting_n": is_waiting_n
        }
        expectedMoveService.update(mapping)
