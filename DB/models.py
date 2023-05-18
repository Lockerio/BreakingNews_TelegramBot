from sqlalchemy import Column, Integer, Table, Text, ForeignKey

from database import engine
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

Favorites = Table('Favorites', Base.metadata,
                  Column('agency_id', Integer(), ForeignKey('NewsAgencies.id')),
                  Column('user_id', Integer(), ForeignKey('Users.id'))
                  )


class NewsAgency(Base):
    __tablename__ = 'NewsAgencies'
    id = Column(Integer(), primary_key=True)
    name = Column(Text())
    description = Column(Text())
    news = relationship("News", back_populates="news_agency")

    def __repr__(self):
        return f'{self.name}'


class User(Base):
    __tablename__ = 'Users'
    id = Column(Integer(), primary_key=True)
    telegram_id = Column(Integer())
    news_amount_to_show = Column(Integer())
    news_agencies = relationship("NewsAgency", secondary=Favorites, backref="users")

    def __repr__(self):
        return f'{self.telegram_id}'


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
