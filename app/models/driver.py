from sqlalchemy import Column, String, Integer, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from app.db.connection import Base

class Driver(Base):
    __tablename__ = 'drivers'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    license_number = Column(String(50), unique=True)
    
    # One-to-one relationship, with vehicle_id as a ForeignKey
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), unique=True, nullable=False)
    total_trips = Column(Integer, default=0)
    total_earnings = Column(Numeric(12, 2), default=0.0)

    # relationship to Vehicle (back_populates on both sides)
    vehicle = relationship("Vehicle", back_populates="driver", uselist=False)

    def __repr__(self):
        return f"Driver({self.name}, {self.license_number})"
