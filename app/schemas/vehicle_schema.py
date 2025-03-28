from pydantic import BaseModel
from typing import Optional

class VehicleBase(BaseModel):
    license_plate: str
    model: str
    capacity: int
    category: str
    status: str = 'active'
    total_trips: int = 0
    total_distance_travelled: float = 0
    manufacture_year: int
    
    # New fields for ML
    fuel_efficiency: Optional[float] = None
    maintenance_score: Optional[float] = None
    last_maintenance_date: Optional[str] = None
    maintenance_frequency: Optional[int] = None
    engine_hours: Optional[float] = None
    idle_time_percentage: Optional[float] = None
    avg_speed: Optional[float] = None
    emissions_data: Optional[str] = None
    tire_wear_rate: Optional[float] = None
    breakdown_frequency: Optional[float] = None
    sensor_data_json: Optional[str] = None
    operational_cost_per_mile: Optional[float] = None
    
    # Foreign keys
    driver_id: Optional[int] = None
    route_id: Optional[int] = None

class VehicleCreate(VehicleBase):
    pass

class VehicleUpdate(BaseModel):
    license_plate: Optional[str] = None
    model: Optional[str] = None
    capacity: Optional[int] = None
    category: Optional[str] = None
    status: Optional[str] = None
    total_trips: Optional[int] = None
    total_distance_travelled: Optional[float] = None
    manufacture_year: Optional[int] = None
    
    # New fields for ML
    fuel_efficiency: Optional[float] = None
    maintenance_score: Optional[float] = None
    last_maintenance_date: Optional[str] = None
    maintenance_frequency: Optional[int] = None
    engine_hours: Optional[float] = None
    idle_time_percentage: Optional[float] = None
    avg_speed: Optional[float] = None
    emissions_data: Optional[str] = None
    tire_wear_rate: Optional[float] = None
    breakdown_frequency: Optional[float] = None
    sensor_data_json: Optional[str] = None
    operational_cost_per_mile: Optional[float] = None
    
    # Foreign keys
    driver_id: Optional[int] = None
    route_id: Optional[int] = None

class VehicleResponse(VehicleBase):
    id: int

    class Config:
        orm_mode = True