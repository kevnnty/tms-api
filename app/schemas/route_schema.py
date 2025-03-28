from pydantic import BaseModel
from typing import Optional

class RouteBase(BaseModel):
    route_code: str
    cost: float
    start_location: str
    end_location: str
    estimated_travel_time: str
    distance: float
    
    # New fields for ML
    avg_traffic_density: Optional[float] = None
    avg_fuel_consumption: Optional[float] = None
    historical_delays: Optional[float] = None
    weather_risk_factor: Optional[float] = None
    time_of_day_efficiency: Optional[str] = None
    day_of_week_efficiency: Optional[str] = None
    seasonal_factors: Optional[str] = None
    complexity_score: Optional[float] = None
    historical_incidents: Optional[int] = None

class RouteCreate(RouteBase):
    pass

class RouteUpdate(BaseModel):
    route_code: Optional[str] = None
    cost: Optional[float] = None
    start_location: Optional[str] = None
    end_location: Optional[str] = None
    estimated_travel_time: Optional[str] = None
    distance: Optional[float] = None
    
    # New fields for ML
    avg_traffic_density: Optional[float] = None
    avg_fuel_consumption: Optional[float] = None
    historical_delays: Optional[float] = None
    weather_risk_factor: Optional[float] = None
    time_of_day_efficiency: Optional[str] = None
    day_of_week_efficiency: Optional[str] = None
    seasonal_factors: Optional[str] = None
    complexity_score: Optional[float] = None
    historical_incidents: Optional[int] = None

class RouteResponse(RouteBase):
    id: int

    class Config:
        orm_mode = True