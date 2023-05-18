from models import Action


class ActionSerializer:
    def __init__(self, session):
        self.session = session

    def get_one(self, action_id):
        return self.session.query(Action).get(action_id)

    def get_all(self):
        return self.session.query(Action).all()

    def create(self, data):
        action = Action(**data)
        self.session.add(action)
        self.session.commit()
        return action
