from sqlalchemy import Column, Integer, Table, Text, ForeignKey, JSON, BOOLEAN


from sqlalchemy.orm import declarative_base, relationship

from database import engine

Base = declarative_base()


class Favorites(Base):
    __tablename__ = 'Favorites'
    id = Column(Integer(), primary_key=True)
    agency_id = Column(Integer(), ForeignKey('NewsAgencies.id'))
    user_id = Column(Integer(), ForeignKey('Users.id'))

    def __repr__(self):
        return f'{self.user_id} {self.agency_id}'


class NewsAgency(Base):
    __tablename__ = 'NewsAgencies'
    id = Column(Integer(), primary_key=True)
    name = Column(Text())
    description = Column(Text())
    beauty_url = Column(Text())
    source_agency = relationship("User", backref="news_agency")
    news = relationship("News", back_populates="news_agency")
    favorites = relationship("Favorites", backref="news_agency")

    def __repr__(self):
        return f'{self.name}'


class User(Base):
    __tablename__ = 'Users'
    id = Column(Integer(), primary_key=True)
    telegram_id = Column(Integer())
    chat_id = Column(Integer())
    news_amount_to_show = Column(Integer(), default=5)
    actions = relationship("Action", backref="users")
    source_agency_id = Column(Integer(), ForeignKey('NewsAgencies.id'))
    expected_moves = relationship("ExpectedMove", backref="users")
    favorites = relationship("Favorites", backref="users")

    def __repr__(self):
        return f"""
            {self.id}
            {self.telegram_id}
            {self.news_amount_to_show}
            {self.news_agencies}
            {self.source_agency_id}
            {self.expected_moves}
        """


class Action(Base):
    __tablename__ = 'Actions'
    id = Column(Integer(), primary_key=True)
    json_description = Column(JSON())
    user_id = Column(Integer(), ForeignKey('Users.id'))

    def __repr__(self):
        return f'{self.json_description}'


class ExpectedMove(Base):
    __tablename__ = 'ExpectedMove'
    id = Column(Integer(), primary_key=True)
    is_waiting_n = Column(BOOLEAN(), default=False)
    amount_of_read_news = Column(Integer(), default=1)
    user_id = Column(Integer(), ForeignKey('Users.id'))

    def __repr__(self):
        return f'{self.is_waiting_n}'


class News(Base):
    __tablename__ = 'News'
    id = Column(Integer(), primary_key=True)
    title = Column(Text())
    text = Column(Text())
    url = Column(Text())
    news_agency_id = Column(Integer(), ForeignKey('NewsAgencies.id'))
    news_agency = relationship("NewsAgency", back_populates="news")

    def __repr__(self):
        return f'{self.title}'


if __name__ == '__main__':
    Base.metadata.create_all(engine, checkfirst=True)
