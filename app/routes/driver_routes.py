from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any
from app.db.connection import SessionLocal
from app.schemas.driver_schema import DriverCreate, DriverResponse, DriverUpdate
from app.services.driver_service import DriverService

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create Driver
@router.post("/", response_model=DriverResponse)
def create_driver(driver: DriverCreate, db: Session = Depends(get_db)):
    db_driver = DriverService.create_driver(db=db, driver_data=driver)
    return db_driver

# List Drivers
@router.get("/", response_model=list[DriverResponse])
def list_drivers(db: Session = Depends(get_db)):
    drivers = DriverService.get_drivers(db=db)
    return drivers

# Get Driver by ID
@router.get("/{driver_id}", response_model=DriverResponse)
def get_driver(driver_id: int, db: Session = Depends(get_db)):
    db_driver = DriverService.get_driver_by_id(db=db, driver_id=driver_id)
    if db_driver is None:
        raise HTTPException(status_code=404, detail="Driver not found")
    return db_driver

# Get Driver by Email
@router.get("/email/{email}", response_model=DriverResponse)
def get_driver_by_email(email: str, db: Session = Depends(get_db)):
    db_driver = DriverService.get_driver_by_email(db=db, email=email)
    if db_driver is None:
        raise HTTPException(status_code=404, detail="Driver not found")
    return db_driver

# Get Driver by License
@router.get("/license/{license_number}", response_model=DriverResponse)
def get_driver_by_license(license_number: str, db: Session = Depends(get_db)):
    db_driver = DriverService.get_driver_by_license(db=db, license_number=license_number)
    if db_driver is None:
        raise HTTPException(status_code=404, detail="Driver not found")
    return db_driver

# Update Driver
@router.put("/{driver_id}", response_model=DriverResponse)
def update_driver(driver_id: int, driver: DriverUpdate, db: Session = Depends(get_db)):
    db_driver = DriverService.update_driver(db=db, driver_id=driver_id, driver_data=driver)
    if db_driver is None:
        raise HTTPException(status_code=404, detail="Driver not found")
    return db_driver

# Delete Driver
@router.delete("/{driver_id}", response_model=DriverResponse)
def delete_driver(driver_id: int, db: Session = Depends(get_db)):
    db_driver = DriverService.delete_driver(db=db, driver_id=driver_id)
    if db_driver is None:
        raise HTTPException(status_code=404, detail="Driver not found")
    return db_driver

# Update ML Metrics
@router.patch("/{driver_id}/ml-metrics", response_model=DriverResponse)
def update_ml_metrics(driver_id: int, metrics: Dict[str, Any], db: Session = Depends(get_db)):
    db_driver = DriverService.update_ml_metrics(db=db, driver_id=driver_id, metrics=metrics)
    if db_driver is None:
        raise HTTPException(status_code=404, detail="Driver not found")
    return db_driver