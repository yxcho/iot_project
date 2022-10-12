from dotenv import load_dotenv
import os
load_dotenv()
import sqlalchemy as db
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


DB_USER = os.getenv("DB_USER")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_PASSW = os.getenv("DB_PASSW")
DB_PORT = os.getenv("DB_PORT")

SQLALCHEMY_DATABASE_URI =  f'postgresql://{DB_USER}:{DB_PASSW}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
engine = db.create_engine(SQLALCHEMY_DATABASE_URI)
connection = engine.connect()

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

print(session)


from sqlalchemy import Table, Column, Integer, String, Float, MetaData, DateTime
meta = MetaData()


light = Table(
    'light', meta, 
    Column('id', Integer, primary_key = True), 
    Column('sensor_id', Integer), 
    Column('timestamp', DateTime), 
    Column('value', Float)
)


meta.create_all(engine)


if __name__ == '__main__':
    # create_tables()
    ...