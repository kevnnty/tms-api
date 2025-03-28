from pydantic import BaseModel
from typing import Optional
from decimal import Decimal

class DriverBase(BaseModel):
    name: str
    email: str
    license_number: str
    total_trips: int = 0
    total_earnings: Decimal = Decimal('0.00')
    
    # New fields for ML
    safety_score: Optional[float] = None
    on_time_delivery_rate: Optional[float] = None
    experience_years: Optional[float] = None
    rest_compliance_rate: Optional[float] = None
    avg_speed_profile: Optional[str] = None
    harsh_braking_events: Optional[int] = None
    harsh_acceleration_events: Optional[int] = None
    fuel_efficiency_score: Optional[float] = None
    route_adherence: Optional[float] = None
    customer_satisfaction: Optional[float] = None
    training_level: Optional[int] = None
    certifications: Optional[str] = None
    preferred_routes: Optional[str] = None
    fatigue_score: Optional[float] = None

class DriverCreate(DriverBase):
    pass

class DriverUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    license_number: Optional[str] = None
    total_trips: Optional[int] = None
    total_earnings: Optional[Decimal] = None
    
    # New fields for ML
    safety_score: Optional[float] = None
    on_time_delivery_rate: Optional[float] = None
    experience_years: Optional[float] = None
    rest_compliance_rate: Optional[float] = None
    avg_speed_profile: Optional[str] = None
    harsh_braking_events: Optional[int] = None
    harsh_acceleration_events: Optional[int] = None
    fuel_efficiency_score: Optional[float] = None
    route_adherence: Optional[float] = None
    customer_satisfaction: Optional[float] = None
    training_level: Optional[int] = None
    certifications: Optional[str] = None
    preferred_routes: Optional[str] = None
    fatigue_score: Optional[float] = None

class DriverResponse(DriverBase):
    id: int

    class Config:
        orm_mode = True