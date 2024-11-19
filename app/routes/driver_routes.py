from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.connection import SessionLocal
from app.schemas.vehicle_schema import VehicleCreate, VehicleResponse
from app.services.vehicle_service import VehicleService

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
        
# Create Vehicle
@router.post("/", response_model=VehicleResponse)
def create_vehicle(vehicle: VehicleCreate, db: Session = Depends(get_db)):
    db_vehicle = VehicleService.create_vehicle(db=db, vehicle_data=vehicle)
    return db_vehicle



# List Vehicles
@router.get("/", response_model=list[VehicleResponse])
def list_vehicles(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    vehicles = VehicleService.get_vehicles(db=db, skip=skip, limit=limit)
    return vehicles


# Get Vehicle by ID
@router.get("/{vehicle_id}", response_model=VehicleResponse)
def get_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    db_vehicle = VehicleService.get_vehicle_by_id(db=db, vehicle_id=vehicle_id)
    if db_vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return db_vehicle
