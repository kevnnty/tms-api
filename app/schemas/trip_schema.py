from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TripBase(BaseModel):
    vehicle_id: int
    driver_id: int
    route_id: int
    
    start_time: datetime
    end_time: Optional[datetime] = None
    actual_duration: Optional[float] = None
    expected_duration: float
    
    start_fuel_level: float
    end_fuel_level: Optional[float] = None
    fuel_consumed: Optional[float] = None
    
    actual_distance: Optional[float] = None
    planned_distance: float
    
    average_speed: Optional[float] = None
    max_speed: Optional[float] = None
    idle_time: Optional[float] = None
    
    weather_conditions: Optional[str] = None
    traffic_conditions: Optional[str] = None
    
    on_time_status: bool = True
    delay_reason: Optional[str] = None
    
    cargo_weight: Optional[float] = None
    cargo_type: Optional[str] = None
    
    maintenance_issues_reported: Optional[str] = None
    incidents_reported: Optional[str] = None
    
    driver_fatigue_score: Optional[float] = None

class TripCreate(TripBase):
    pass

class TripUpdate(BaseModel):
    vehicle_id: Optional[int] = None
    driver_id: Optional[int] = None
    route_id: Optional[int] = None
    
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    actual_duration: Optional[float] = None
    expected_duration: Optional[float] = None
    
    start_fuel_level: Optional[float] = None
    end_fuel_level: Optional[float] = None
    fuel_consumed: Optional[float] = None
    
    actual_distance: Optional[float] = None
    planned_distance: Optional[float] = None
    
    average_speed: Optional[float] = None
    max_speed: Optional[float] = None
    idle_time: Optional[float] = None
    
    weather_conditions: Optional[str] = None
    traffic_conditions: Optional[str] = None
    
    on_time_status: Optional[bool] = None
    delay_reason: Optional[str] = None
    
    cargo_weight: Optional[float] = None
    cargo_type: Optional[str] = None
    
    maintenance_issues_reported: Optional[str] = None
    incidents_reported: Optional[str] = None
    
    driver_fatigue_score: Optional[float] = None

class TripResponse(TripBase):
    id: int

    class Config:
        orm_mode = True