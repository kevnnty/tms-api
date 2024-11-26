from sqlalchemy import Column, String, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.db.connection import Base

class Vehicle(Base):
    __tablename__ = 'vehicles'

    id = Column(Integer, primary_key=True, index=True)
    license_plate = Column(String(15), unique=True, index=True)
    model = Column(String(50))
    capacity = Column(Integer)
    category = Column(String(50))
    status = Column(String(20), default='active')
    total_trips = Column(Integer)
    total_distance_travelled = Column(Float)
    manufacture_year = Column(Integer)

    driver_id = Column(Integer, ForeignKey("drivers.id"), unique=True, nullable=True)
    route_id = Column(Integer, ForeignKey("routes.id"), nullable=True)

    driver = relationship("Driver", back_populates="vehicles")
    route = relationship("Route", back_populates="vehicles")
