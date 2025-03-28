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
    company_name = Column(String)
    # New fields for ML
    fuel_efficiency = Column(Float)  # Miles per gallon or equivalent
    maintenance_score = Column(Float)  # Health score (0-1)
    last_maintenance_date = Column(String(50))  # Date of last maintenance
    maintenance_frequency = Column(Integer)  # Average days between maintenance
    engine_hours = Column(Float)  # Total engine hours
    idle_time_percentage = Column(Float)  # Percentage of time spent idling
    avg_speed = Column(Float)  # Average operational speed
    emissions_data = Column(String(200))  # JSON string with emissions metrics
    tire_wear_rate = Column(Float)  # Rate of tire wear
    breakdown_frequency = Column(Float)  # Breakdowns per 1000 miles
    sensor_data_json = Column(String(500))  # JSON string with latest sensor readings
    operational_cost_per_mile = Column(Float)  # Cost per mile to operate

    driver_id = Column(Integer, ForeignKey("drivers.id"), unique=True, nullable=True)
    route_id = Column(Integer, ForeignKey("routes.id"), nullable=True)

    driver = relationship("Driver", back_populates="vehicles")
    route = relationship("Route", back_populates="vehicles")