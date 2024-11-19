from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.connection import SessionLocal
from app.models.vehicle import Vehicle
from app.schemas.vehicle import VehicleCreate, VehicleResponse
from app.services.vehicle_service import create_vehicle_service, list_vehicles_service

router = APIRouter(prefix="/vehicles")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=VehicleResponse)
def create_vehicle(vehicle: VehicleCreate, db: Session = Depends(get_db)):
    return create_vehicle_service(vehicle, db)

@router.get("/", response_model=list[VehicleResponse])
def list_vehicles(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return list_vehicles_service(skip, limit, db)    
