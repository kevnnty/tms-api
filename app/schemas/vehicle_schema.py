from pydantic import BaseModel
from typing import Optional

class VehicleBase(BaseModel):
    license_plate: str
    model: str
    capacity: int
    category: str = 'taxi'  # Default value
    status: str = 'active'  # Default value
    total_trips: int = 0
    total_distance: float = 0.0

class VehicleCreate(VehicleBase):
    route_id: Optional[int] = None

class VehicleResponse(VehicleBase):
    id: int

    class Config:
        orm_mode = True
