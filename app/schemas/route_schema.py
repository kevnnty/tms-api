from pydantic import BaseModel
from typing import List, Optional

class RouteCreate(BaseModel):
    start_location: str
    end_location: str
    estimated_travel_time: int  # in minutes
    distance: float  # in kilometers
    start_time: str
    end_time: str

    class Config:
        orm_mode = True

class RouteResponse(RouteCreate):
    id: int
    vehicles: List[int]  # List of vehicle IDs associated with this route

    class Config:
        orm_mode = True
