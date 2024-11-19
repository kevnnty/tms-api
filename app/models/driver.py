from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.db.connection import Base

class Driver(Base):
    __tablename__ = "drivers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    phone_number = Column(String)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"))

    vehicle = relationship("Vehicle", back_populates="drivers")
