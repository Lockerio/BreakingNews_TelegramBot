from serializers.action_serializer import ActionSerializer


class ActionService:
    def __init__(self, serializer: ActionSerializer):
        self.serializer = serializer

    def get_one(self, action_id):
        return self.serializer.get_one(action_id)

    def get_all(self):
        return self.serializer.get_all()

    def create(self, data):
        return self.serializer.create(data)
