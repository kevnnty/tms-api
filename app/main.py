from fastapi import FastAPI
from app.routes import utilities_routes, vehicle_routes, driver_routes, route_routes, trip_routes, prediction_routes
from app.db.connection import Base, engine

# Create FastAPI app
app = FastAPI(
    title="TMS | Transport Management System",
    description="Transport Management System with accident risk prediction"
)

# Create all tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(vehicle_routes.router, prefix="/vehicles", tags=["vehicles"])
app.include_router(driver_routes.router, prefix="/drivers", tags=["drivers"])
app.include_router(route_routes.router, prefix="/routes", tags=["routes"])
app.include_router(trip_routes.router, prefix="/trips", tags=["trips"])
app.include_router(prediction_routes.router, prefix="/ml", tags=["prediction"])
app.include_router(utilities_routes.router, tags=["utilities"])
