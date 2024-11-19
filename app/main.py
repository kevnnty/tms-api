from fastapi import FastAPI
from app.routes import vehicle_routes, driver_routes, route_routes

app = FastAPI(
  title="TMS | Transport Manangement System",
  description=""
)

app.include_router(vehicle_routes.router, prefix="/vehicles", tags=["vehicles"])
app.include_router(driver_routes.router, prefix="/drivers", tags=["drivers"])
app.include_router(route_routes.router, prefix="/routes", tags=["routes"])