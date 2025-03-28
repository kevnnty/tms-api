from sqlalchemy import Column, String, Integer, Numeric, Float
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

    # New fields for ML
    safety_score = Column(Float)  # Safety rating (0-1)
    on_time_delivery_rate = Column(Float)  # Percentage of on-time deliveries
    experience_years = Column(Float)  # Years of driving experience
    rest_compliance_rate = Column(Float)  # Compliance with rest periods (0-1)
    avg_speed_profile = Column(String(200))  # JSON string with speed patterns
    harsh_braking_events = Column(Integer)  # Count of harsh braking incidents
    harsh_acceleration_events = Column(Integer)  # Count of harsh acceleration events
    fuel_efficiency_score = Column(Float)  # Driver's impact on fuel efficiency (0-1)
    route_adherence = Column(Float)  # How closely driver follows planned routes (0-1)
    customer_satisfaction = Column(Float)  # Average customer satisfaction (0-5)
    training_level = Column(Integer)  # Level of training completed (1-5)
    certifications = Column(String(200))  # JSON string with certification data
    preferred_routes = Column(String(200))  # JSON string with route preferences
    fatigue_score = Column(Float)  # Estimated fatigue level based on work hours (0-1)

    vehicles = relationship("Vehicle", back_populates="driver", uselist=True)