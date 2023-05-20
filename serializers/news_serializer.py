from models import News


class NewsSerializer:
    def __init__(self, session):
        self.session = session

    def get_one(self, news_id):
        return self.session.query(News).get(news_id)

    def get_one_by_title(self, title):
        return self.session.query(News).filter_by(title=title).first()

    def get_all(self):
        return self.session.query(News).all()

    def create(self, data):
        news = News(**data)
        self.session.add(news)
        self.session.commit()
        return news

    def update(self, news):
        self.session.add(news)
        self.session.commit()
        return news

    def delete(self, news_id):
        news = self.get_one(news_id)
        self.session.delete(news)
        self.session.commit()
