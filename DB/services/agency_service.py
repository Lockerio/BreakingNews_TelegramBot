from DB.serializers.agency_serializer import AgencySerializer


class NewsService:
    def __init__(self, serializer: AgencySerializer):
        self.serializer = serializer

    def get_one(self, agency_id):
        return self.serializer.get_one(agency_id)

    def get_all(self):
        return self.serializer.get_all()

    def create(self, data):
        return self.serializer.create(data)

    def update(self, data):
        agency_id = data.get("id")
        agency = self.get_one(agency_id)
        agency.name = data.get("title")
        agency.description = data.get("description")
        return self.serializer.update(agency)

    def delete(self, agency_id):
        self.serializer.delete(agency_id)
