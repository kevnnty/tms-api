from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.orm import relationship
from app.db.connection import Base

class Route(Base):
    __tablename__ = "routes"

    id = Column(Integer, primary_key=True, index=True)
    route_name = Column(String, unique=True, index=True)
    start_location = Column(String)
    end_location = Column(String)
    estimated_travel_time = Column(Float)  # Estimated travel time in hours
    distance = Column(Float)  # Distance in kilometers

    vehicles = relationship("Vehicle", back_populates="route")
