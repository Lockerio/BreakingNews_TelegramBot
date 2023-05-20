from models import ExpectedMove


class ExpectedMoveSerializer:
    def __init__(self, session):
        self.session = session

    def get_one(self, expected_move_id):
        return self.session.query(ExpectedMove).get(expected_move_id)

    def get_one_by_user_id(self, user_id):
        return self.session.query(ExpectedMove).filter_by(user_id=user_id).first()

    def get_all(self):
        return self.session.query(ExpectedMove).all()

    def create(self, data):
        expected_move = ExpectedMove(**data)
        self.session.add(expected_move)
        self.session.commit()
        return expected_move

    def update(self, expected_move):
        self.session.add(expected_move)
        self.session.commit()
        return expected_move

    def delete(self, expected_move_id):
        expected_move = self.get_one(expected_move_id)
        self.session.delete(expected_move)
        self.session.commit()
