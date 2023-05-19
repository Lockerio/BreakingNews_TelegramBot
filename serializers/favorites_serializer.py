from models import Favorites


class FavoritesSerializer:
    def __init__(self, session):
        self.session = session

    def get_one(self, favorites_id):
        return self.session.query(Favorites).get(favorites_id)

    def get_all(self):
        return self.session.query(Favorites).all()

    def create(self, data):
        favorites = Favorites(**data)
        self.session.add(favorites)
        self.session.commit()
        return favorites

    def delete(self, favorites_id):
        favorites = self.get_one(favorites_id)
        self.session.delete(favorites)
        self.session.commit()