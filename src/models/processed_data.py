
from email.policy import default
from src.data import Base
from sqlalchemy import Column, Integer, String, Time, Float, DateTime
from sqlalchemy.sql import func

class Processed_data(Base):
    __tablename__ = "processed_data"
    carriage_id = Column(Integer)
    comfort_indicator = Column(String)
    value = Column(Integer)
    timestamp = Column(DateTime(timezone=True), default=func.clock_timestamp())