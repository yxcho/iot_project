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
    Column('no_seat',Integer,server_default='50'),
    Column('capacity',Integer,server_default='300')
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


class Carriage(Base):
    __tablename__ = "carriage"
    carriage_id = Column(Integer,primary_key=True)
    train_id = Column(Integer)
    no_seat = Column(Integer,server_default='50')
    capacity = Column(Integer,server_default='300')


class Train(Base):
    __tablename__ = "train"
    train_line = Column(String)
    train_id = Column(Integer,primary_key=True)
    no_carriage = Column(Integer)


def populate_train():
    blue_line = Train(train_line = "B", no_carriage = 3)
    blue_line1 = Train(train_line = "B", no_carriage = 3)
    red_line = Train(train_line = "R", no_carriage = 6)
    red_line1 = Train(train_line = "R", no_carriage = 6)
    green_line = Train(train_line = "G", no_carriage = 6)
    green_line1 = Train(train_line = "G", no_carriage = 6)
    

    lines = [blue_line,blue_line1, green_line,green_line1, red_line,red_line1]
    session = sessionmaker(bind=engine)()
    session.add_all(lines)
    session.commit()

def populate_carriage():
    x = [1,1,1,2,2,2,3,3,3,3,3,4,4,4,4,4,5,5,5,5,5,6,6,6,6,6]
    lines = []
    
    for id in x:
        c = Carriage(train_id = id)
        lines.append(c)

    session = sessionmaker(bind=engine)()
    session.add_all(lines)
    session.commit()



if __name__ == '__main__':
    meta.create_all(engine)
    populate_train()
    populate_carriage()
