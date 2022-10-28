
from src.data import Base
from sqlalchemy import Column, Integer, String, Time, Float, DateTime
from sqlalchemy.sql import func

class Processed_data(Base):
    __tablename__ = 'processed_data'
    id = Column(Integer, primary_key=True) #, autoincrement=True)
    carriage_id = Column("carriage_id", Integer)
    comfort_indicator = Column("comfort_indicator", String)
    value = Column("value", Float)
    timestamp = Column("timestamp", DateTime(timezone=True), default=func.clock_timestamp())
