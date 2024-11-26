from pydantic import BaseModel
from typing import Optional

class VehicleBase(BaseModel):
    license_plate: str
    model: Optional[str]
    capacity: int
    category: str
    status: str = 'active'  # Default value
    total_trips: Optional[int] = 0
    total_distance_travelled: Optional[float] = 0.0
    manufacture_year: int

class VehicleCreate(VehicleBase):
    route_id: Optional[int] = None  # Optional route ID during creation
    total_trips: Optional[int] = None
    total_distance_travelled: Optional[float] = None
    model: Optional[str] = None

class VehicleResponse(VehicleBase):
    id: int

    class Config:
        orm_mode = True
