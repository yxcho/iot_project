import os
from dotenv import load_dotenv
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


train = Table(
    'train', meta, 
    Column('train_line',String),
    Column('train_id',Integer,primary_key=True),
    Column('no_carriage',Integer)
)

carriage = Table(
    'carriage', meta, 
    Column('carriage_id',Integer,primary_key=True),
    Column('train_id',Integer),
    Column('no_seat',Integer,server_default='10'),
    Column('capacity',Integer,server_default='40')
)

processed_data = Table(
    'processed_data', meta, 
    Column('carriage_id',Integer),
    Column('comfort_indicator',String),
    Column('value',Integer),
    Column('timestamp', DateTime)
)

sensors_data = Table(
    'sensors_data', meta, 
    Column('carriage_id',Integer),
    Column('sensor_id',Integer),
    Column('sensor_type',String),
    Column('comfort_indicator',String),
    Column('value',Float),
    Column('timestamp', DateTime)
)


meta.create_all(engine)


if __name__ == '__main__':
    #create_tables()
    ...