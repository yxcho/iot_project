
from src.data import Base
from sqlalchemy import Column, Integer, String, Time, Float, DateTime
from sqlalchemy.sql import func

class Crowd(Base):
    __tablename__ = "crowd"
    #id = Column(Integer, primary_key=True)
    train_line = Column(String)
    train_id = Column(Integer)
    carriage_id = Column(Integer)
    density = Column(Integer)
    timestamp = Column(DateTime(timezone=True), default=func.clock_timestamp())