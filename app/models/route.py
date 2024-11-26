from sqlalchemy import Column, String, Float, Interval, Integer
from sqlalchemy.orm import relationship
from app.db.connection import Base

class Route(Base):
    __tablename__ = 'routes'

    id = Column(Integer, primary_key=True, index=True)
    route_code = Column(String(50), unique=True)
    cost = Column(Float)
    start_location = Column(String(100))
    end_location = Column(String(100))
    estimated_travel_time = Column(String(100))
    distance = Column(Float)
    
    # Relationship with Vehicle
    vehicles = relationship("Vehicle", back_populates="route", uselist=True)
