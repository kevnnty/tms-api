from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.connection import SessionLocal
from app.schemas.driver_schema import DriverCreate, DriverResponse
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



@router.put("/{driver_id}/assign-vehicle/{vehicle_id}")
def assign_vehicle(driver_id: int, vehicle_id: int, db: Session = Depends(get_db)):
    try:
        driver = DriverService.assign_vehicle_to_driver(db, driver_id, vehicle_id)
        return driver
    except HTTPException as e:
        raise e