from pydantic import BaseModel
from typing import Optional

class DriverBase(BaseModel):
    name: str
    email: str
    license_number: str
    total_trips: Optional[int] = 0
    total_earnings: Optional[float] = 0.0

class DriverCreate(DriverBase):
    pass

class DriverResponse(DriverBase):
    id: int

    class Config:
        orm_mode = True
