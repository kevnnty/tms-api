from pydantic import BaseModel

class RouteBase(BaseModel):
    start_location: str
    end_location: str
    estimated_travel_time: str
    distance: float

class RouteCreate(RouteBase):
    pass

class RouteResponse(RouteBase):
    id: int

    class Config:
        orm_mode = True
