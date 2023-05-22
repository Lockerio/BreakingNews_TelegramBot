from serializers.favorites_serializer import FavoritesSerializer


class FavoritesService:
    def __init__(self, serializer: FavoritesSerializer):
        self.serializer = serializer

    def get_one(self, favorites_id):
        return self.serializer.get_one(favorites_id)

    def get_one_by_user_and_agency(self, user_id, agency_id):
        return self.serializer.get_one_by_user_and_agency(user_id, agency_id)

    def get_all(self):
        return self.serializer.get_all()

    def create(self, data):
        if self.get_one_by_user_and_agency(data["user_id"], data["agency_id"]):
            return
        return self.serializer.create(data)

    def delete(self, user_id, agency_id):
        self.serializer.delete(user_id, agency_id)
