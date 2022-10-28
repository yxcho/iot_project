
from src.data import Base
from sqlalchemy import Column, Integer, String, Time, Float, DateTime
from sqlalchemy.sql import func


class Sensors_data(Base):
    __tablename__ = "sensors_data"
    id = Column(Integer,primary_key=True)
    carriage_id = Column(Integer)
    sensor_id = Column(String)
    sensor_type = Column(String)
    comfort_indicator = Column(String)
    value = Column(Integer)
    timestamp = Column(DateTime(timezone=True), default=func.clock_timestamp())
