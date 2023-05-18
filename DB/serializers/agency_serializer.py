from DB.models import NewsAgency


class AgencySerializer:
    def __init__(self, session):
        self.session = session

    def get_one(self, agency_id):
        return self.session.query(NewsAgency).get(agency_id)

    def get_all(self):
        return self.session.query(NewsAgency).all()

    def create(self, data):
        agency = NewsAgency(**data)
        self.session.add(agency)
        self.session.commit()
        return agency

    def update(self, agency):
        self.session.add(agency)
        self.session.commit()
        return agency

    def delete(self, agency_id):
        agency = self.get_one(agency_id)
        self.session.delete(agency)
        self.session.commit()
