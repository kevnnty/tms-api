from pydantic import BaseModel
from typing import Optional

class DriverCreate(BaseModel):
    first_name: str
    last_name: str
    license_number: str
    phone_number: Optional[str] = None

    class Config:
        orm_mode = True

class DriverResponse(DriverCreate):
    id: int
    vehicle_id: Optional[int]  # Optional, as drivers may or may not be assigned to a vehicle

    class Config:
        orm_mode = True
