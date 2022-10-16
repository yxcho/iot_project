
from src.data import Base
from sqlalchemy import Column, Integer, String, Time, Float, DateTime
from sqlalchemy.sql import func

class Seat(Base):
    __tablename__ = "seat_raw"
    #id = Column(Integer, primary_key=True)
    train_line = Column(String)
    train_id = Column(Integer)
    carriage_id = Column(Integer)
    sensor_id = Column(Integer)
    value = Column(Float)
    timestamp = Column(DateTime(timezone=True), default=func.clock_timestamp())