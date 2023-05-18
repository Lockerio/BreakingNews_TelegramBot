from serializers.favorites_serializer import FavoritesSerializer


class FavoritesService:
    def __init__(self, serializer: FavoritesSerializer):
        self.serializer = serializer

    def get_one(self, favorites_id):
        return self.serializer.get_one(favorites_id)

    def get_all(self):
        return self.serializer.get_all()

    def create(self, data):
        return self.serializer.create(data)

    def delete(self, favorites_id):
        self.serializer.delete(favorites_id)
