from models import Favorites


class FavoritesSerializer:
    def __init__(self, session):
        self.session = session

    def get_one(self, favorites_id):
        return self.session.query(Favorites).get(favorites_id)

    def get_one_by_user_and_agency(self, user_id, agency_id):
        return self.session.query(Favorites).\
            filter_by(user_id=user_id).\
            filter_by(agency_id=agency_id).\
            first()

    def get_all(self):
        return self.session.query(Favorites).all()

    def get_all_by_agency_id(self, agency_id):
        return self.session.query(Favorites).filter_by(agency_id=agency_id).all()

    def create(self, data):
        favorites = Favorites(**data)
        self.session.add(favorites)
        self.session.commit()
        return favorites

    def delete(self, user_id, agency_id):
        favorite = self.get_one_by_user_and_agency(user_id, agency_id)
        self.session.delete(favorite)
        self.session.commit()
