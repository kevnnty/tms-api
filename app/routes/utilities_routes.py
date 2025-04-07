from fastapi import APIRouter
from tms_model.scripts import generate_dataset

router = APIRouter()

@router.post("/generate-data")
def generate_data(num_routes: int = 10, num_vehicles: int = 20,
                  num_drivers: int = 15, num_trips: int = 100):
    return generate_dataset(
        num_routes=num_routes,
        num_vehicles=num_vehicles,
        num_drivers=num_drivers,
        num_trips=num_trips
    )
