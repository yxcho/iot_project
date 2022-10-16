
from src.data import Base
from sqlalchemy import Column, Integer, String, Time, Float, DateTime
from sqlalchemy.sql import func

class Seat(Base):
    __tablename__ = "seat"
    #id = Column(Integer, primary_key=True)
    train_line = Column(String)
    train_id = Column(Integer)
    carriage_id = Column(Integer)
    seat_id = Column(Integer)
    status = Column(String)
    timestamp = Column(DateTime(timezone=True), default=func.clock_timestamp())