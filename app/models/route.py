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
    estimated_travel_time = Column(Integer) # in hours
    distance = Column(Float)
    
    # New fields for ML
    avg_traffic_density = Column(Float)  # Historical traffic density (0-1 scale)
    avg_fuel_consumption = Column(Float)  # Average fuel used on this route
    historical_delays = Column(Float)  # Average historical delay in minutes
    weather_risk_factor = Column(Float)  # Impact of weather on this route (0-1)
    time_of_day_efficiency = Column(String(100))  # JSON string storing efficiency by hour
    day_of_week_efficiency = Column(String(100))  # JSON string storing efficiency by day
    seasonal_factors = Column(String(100))  # JSON string with seasonal impact data
    complexity_score = Column(Float)  # Route complexity (turns, traffic lights, etc.)
    historical_incidents = Column(Integer)  # Number of incidents on this route
    
    # Relationship with Vehicle
    vehicles = relationship("Vehicle", back_populates="route", uselist=True)