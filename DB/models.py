from sqlalchemy import Column, Integer

from database import db

users = db.Table("Пользователи", db.MetaData(),
                 Column("user_id", Integer, primary_key=True)


                 )

if __name__ == '__main__':
    pass
