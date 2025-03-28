from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.db.connection import Base

class Trip(Base):
    __tablename__ = 'trips'

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"))
    driver_id = Column(Integer, ForeignKey("drivers.id"))
    route_id = Column(Integer, ForeignKey("routes.id"))
    
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    actual_duration = Column(Float)  # In minutes
    expected_duration = Column(Float)  # In minutes
    
    start_fuel_level = Column(Float)
    end_fuel_level = Column(Float)
    fuel_consumed = Column(Float)
    
    actual_distance = Column(Float)
    planned_distance = Column(Float)
    
    average_speed = Column(Float)
    max_speed = Column(Float)
    idle_time = Column(Float)  # In minutes
    
    weather_conditions = Column(String(100))
    traffic_conditions = Column(String(100))
    
    on_time_status = Column(Boolean, default=True)
    delay_reason = Column(String(200), nullable=True)
    
    cargo_weight = Column(Float)
    cargo_type = Column(String(100))
    
    maintenance_issues_reported = Column(String(200))
    incidents_reported = Column(String(200))
    
    driver_fatigue_score = Column(Float)  # Estimated fatigue at trip start (0-1)
    
    # Relationships
    vehicle = relationship("Vehicle")
    driver = relationship("Driver")
    route = relationship("Route")