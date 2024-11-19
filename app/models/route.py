from sqlalchemy import Column, String, Float, Interval, Integer
from app.db.connection import Base
from sqlalchemy.orm import relationship

class Route(Base):
    __tablename__ = 'routes'

    id = Column(Integer, primary_key=True, index=True)
    start_location = Column(String(100))
    end_location = Column(String(100))
    estimated_travel_time = Column(Interval)
    distance = Column(Float)