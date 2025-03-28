from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any
from app.db.connection import SessionLocal
from app.schemas.vehicle_schema import VehicleCreate, VehicleResponse, VehicleUpdate
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
def list_vehicles(db: Session = Depends(get_db)):
    vehicles = VehicleService.get_vehicles(db=db)
    return vehicles

# Get Vehicle by ID
@router.get("/{vehicle_id}", response_model=VehicleResponse)
def get_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    db_vehicle = VehicleService.get_vehicle_by_id(db=db, vehicle_id=vehicle_id)
    if db_vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return db_vehicle

# Get Vehicle by License Plate
@router.get("/license/{license_plate}", response_model=VehicleResponse)
def get_vehicle_by_license(license_plate: str, db: Session = Depends(get_db)):
    db_vehicle = VehicleService.get_vehicle_by_license_plate(db=db, license_plate=license_plate)
    if db_vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return db_vehicle

# Update Vehicle
@router.put("/{vehicle_id}", response_model=VehicleResponse)
def update_vehicle(vehicle_id: int, vehicle: VehicleUpdate, db: Session = Depends(get_db)):
    db_vehicle = VehicleService.update_vehicle(db=db, vehicle_id=vehicle_id, vehicle_data=vehicle)
    if db_vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return db_vehicle

# Delete Vehicle
@router.delete("/{vehicle_id}", response_model=VehicleResponse)
def delete_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    db_vehicle = VehicleService.delete_vehicle(db=db, vehicle_id=vehicle_id)
    if db_vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return db_vehicle

# Update ML Metrics
@router.patch("/{vehicle_id}/ml-metrics", response_model=VehicleResponse)
def update_ml_metrics(vehicle_id: int, metrics: Dict[str, Any], db: Session = Depends(get_db)):
    db_vehicle = VehicleService.update_ml_metrics(db=db, vehicle_id=vehicle_id, metrics=metrics)
    if db_vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return db_vehicle