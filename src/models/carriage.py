
from email.policy import default
from src.data import Base
from sqlalchemy import Column, Integer, String, Time, Float, DateTime
from sqlalchemy.sql import func

class Carriage(Base):
    __tablename__ = "carriage"
    carriage_id = Column(Integer,primary_key=True)
    train_id = Column(Integer)
    no_seat = Column(Integer,server_default='10')
    capacity = Column(Integer,server_default='40')