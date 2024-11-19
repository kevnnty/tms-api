from pydantic import BaseModel

class VehicleBase(BaseModel):
    license_plate: str
    model: str
    capacity: int
    status: str = "available"

class VehicleCreate(VehicleBase):
    pass

class VehicleResponse(VehicleBase):
    id: int

    class Config:
        orm_mode = True
