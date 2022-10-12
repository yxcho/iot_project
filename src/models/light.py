
from src.data import Base
from sqlalchemy import Column, Integer, String, Time, Float, DateTime
from sqlalchemy.sql import func

class Light(Base):
    __tablename__ = "light"
    id = Column(Integer, primary_key=True)
    sensor_id = Column(Integer)
    timestamp = Column(DateTime(timezone=True), default=func.clock_timestamp())
    value = Column(Float)