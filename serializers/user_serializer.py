from models import User


class UserSerializer:
    def __init__(self, session):
        self.session = session

    def get_one(self, user_id):
        return self.session.query(User).get(user_id)

    def get_one_by_telegram_id(self, telegram_id):
        return self.session.query(User).filter_by(telegram_id=telegram_id).first()

    def get_all(self):
        return self.session.query(User).all()

    def get_user_by_source_agency_id(self, source_agency_id):
        return self.session.query(User).filter_by(source_agency_id=source_agency_id).all()

    def create(self, data):
        user = User(**data)
        self.session.add(user)
        self.session.commit()
        return user

    def update(self, user):
        self.session.add(user)
        self.session.commit()
        return user

    def delete(self, user_id):
        user = self.get_one(user_id)
        self.session.delete(user)
        self.session.commit()
