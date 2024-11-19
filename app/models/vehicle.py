from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.db.connection import Base

class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    license_plate = Column(String, unique=True, index=True)
    model = Column(String)
    capacity = Column(Integer)
    status = Column(String, default="available")  # "available", "maintenance"
    # route_id = Column(Integer, ForeignKey("routes.id"))

    # route = relationship("Route", back_populates="vehicles")
