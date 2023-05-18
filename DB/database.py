import sqlalchemy as db


engine = db.create_engine('sqlite:///news.db')

metadata = db.MetaData()






if __name__ == '__main__':
    pass
