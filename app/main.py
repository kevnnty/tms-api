from fastapi import FastAPI, APIRouter
from app.routes import vehicle_routes, driver_routes, route_routes, trip_routes
from app.db.connection import Base, engine
from tms_model.scripts import generate_dataset

app = FastAPI(
  title="TMS | Transport Manangement System",
  description=""
)

# Create all tables
Base.metadata.create_all(bind=engine)


app.include_router(route_routes.router, prefix="/routes", tags=["routes"])
app.include_router(vehicle_routes.router, prefix="/vehicles", tags=["vehicles"])
app.include_router(driver_routes.router, prefix="/drivers", tags=["drivers"])
app.include_router(trip_routes.router, prefix="/trips", tags=["trips"])

# Data generation endpoint
@app.post("/generate-data", tags=["utilities"])
def generate_data(num_routes: int = 10, num_vehicles: int = 20, 
                 num_drivers: int = 15, num_trips: int = 100):
    return generate_dataset(
        num_routes=num_routes,
        num_vehicles=num_vehicles,
        num_drivers=num_drivers,
        num_trips=num_trips
    )