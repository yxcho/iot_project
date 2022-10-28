from dotenv import load_dotenv
import os
load_dotenv()
import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker



DB_USER = os.getenv("DB_USER")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_PASSW = os.getenv("DB_PASSW")
DB_PORT = os.getenv("DB_PORT")

SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASSW}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
print(SQLALCHEMY_DATABASE_URI)
engine = db.create_engine(SQLALCHEMY_DATABASE_URI)
connection = engine.connect()

Session = sessionmaker(expire_on_commit=False)
Session.configure(bind=engine)
session = Session()
Base = declarative_base()

print(session)

