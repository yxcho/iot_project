
from email.policy import default
from src.data import Base
from sqlalchemy import Column, Integer, String, Time, Float, DateTime
from sqlalchemy.sql import func

class Sensors_data(Base):
    __tablename__ = "sensors_data"
    carriage_id = Column(Integer)
    sensor_id = Column(Integer)
    sensor_type = Column(String)
    comfort_indicator = Column(String)
    value = Column(Float)
    timestamp = Column(DateTime(timezone=True), default=func.clock_timestamp())