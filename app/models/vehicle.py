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
    route_id = Column(Integer, ForeignKey("routes.id"), nullable=True)

    total_trips = Column(Integer, default=0)
    total_distance = Column(Float, default=0.0)
    
    # One-to-one relationship, with driver assigned to this vehicle
    driver = relationship("Driver", back_populates="vehicle", uselist=False)

    def __repr__(self):
        return f"Vehicle({self.license_plate}, {self.model})"
