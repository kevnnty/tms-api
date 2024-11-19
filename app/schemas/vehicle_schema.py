from pydantic import BaseModel
from typing import Optional

class VehicleCreate(BaseModel):
    license_plate: str
    model: str
    capacity: int
    status: Optional[str] = "available"  # default value can be "available"

    class Config:
        orm_mode = True  # Tells Pydantic to treat SQLAlchemy models as dictionaries

class VehicleResponse(VehicleCreate):
    id: int  # Include the ID field in the response

    class Config:
        orm_mode = True
