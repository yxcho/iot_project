
from email.policy import default
from src.data import Base
from sqlalchemy import Column, Integer, String, Time, Float, DateTime
from sqlalchemy.sql import func

class Train(Base):
    __tablename__ = "train"
    train_line = Column(String)
    train_id = Column(Integer,primary_key=True)
    no_carriage = Column(Integer)
