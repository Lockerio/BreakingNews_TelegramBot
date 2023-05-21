from models import News
from sqlalchemy import desc


class NewsSerializer:
    def __init__(self, session):
        self.session = session

    def get_one(self, news_id):
        return self.session.query(News).get(news_id)

    def get_one_by_title(self, title):
        return self.session.query(News).filter_by(title=title).first()

    def get_newest_agency_news(self, agency_id):
        latest_news = self.session.query(News).filter_by(news_agency_id=agency_id).order_by(
            desc(News.id)).first()
        return latest_news

    def get_special_news(self, agency_id, amount_of_read_news):
        special_news = self.session.query(News).filter_by(news_agency_id=agency_id).order_by(
            desc(News.id)).offset(amount_of_read_news).first()
        return special_news

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
