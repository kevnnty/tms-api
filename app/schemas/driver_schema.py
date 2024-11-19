from pydantic import BaseModel
from typing import Optional

class DriverBase(BaseModel):
    name: str
    license_number: str
    total_trips: int = 0
    total_earnings: float = 0.0

class DriverCreate(DriverBase):
    vehicle_id: Optional[int] = None

class DriverResponse(DriverBase):
    id: int

    class Config:
        orm_mode = True
