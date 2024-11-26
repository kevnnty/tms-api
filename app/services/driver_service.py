from sqlalchemy.orm import Session
from app.models.driver import Driver
from app.schemas.driver_schema import DriverCreate
from app.models.vehicle import Vehicle
from fastapi import HTTPException

class DriverService:
    
    
    def create_driver(db: Session, driver_data: DriverCreate):
        driver = Driver(**driver_data.dict())
        db.add(driver)
        db.commit()
        db.refresh(driver)
        return driver

    
    
    def get_drivers(db: Session):
        return db.query(Driver).all()

    
    
    def get_driver_by_id(db: Session, driver_id: int):
        driver = db.query(Driver).filter(Driver.id == driver_id).first()
        
        if not driver:
            raise HTTPException(status_code=404, detail="Driver not found")
        
        return driver
    

    
    
    def update_driver(db: Session, driver_id: int, driver_data: DriverCreate):
        driver = db.query(Driver).filter(Driver.id == driver_id).first()
        
        if not driver:
           raise HTTPException(status_code=404, detail="Driver not found")
       
        if driver:
            for key, value in driver_data.dict().items():
                setattr(driver, key, value)
            db.commit()
            db.refresh(driver)
        return driver

    
    
    def delete_driver(db: Session, driver_id: int):
        driver = db.query(Driver).filter(Driver.id == driver_id).first()
        
        if not driver:
            raise HTTPException(status_code=404, detail="Driver not found")
        
        if driver:
            db.delete(driver)
            db.commit()
        return driver


    def assign_vehicle_to_driver(db: Session, driver_id: int, vehicle_id: int):
        driver = db.query(Driver).filter(Driver.id == driver_id).first()
        vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()

        if not driver:
            raise HTTPException(status_code=404, detail="Driver not found")
        
        if not vehicle:
            raise HTTPException(status_code=404, detail="Vehicle not found")
        
        vehicle.driver_id = driver.id
        db.add(vehicle)
        db.commit()
        db.refresh(vehicle)
        
        return driver