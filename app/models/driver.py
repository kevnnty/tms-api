from sqlalchemy import Column, String, Integer, Numeric
from sqlalchemy.orm import relationship
from app.db.connection import Base

class Driver(Base):
    __tablename__ = 'drivers'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100), unique=True)
    license_number = Column(String(50), unique=True)
    total_trips = Column(Integer)
    total_earnings = Column(Numeric(12, 2))

    vehicles = relationship("Vehicle", back_populates="driver", uselist=True)
