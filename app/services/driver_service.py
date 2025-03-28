from sqlalchemy.orm import Session
from app.models.driver import Driver
from app.schemas.driver_schema import DriverCreate, DriverUpdate
from typing import Dict, Any

class DriverService:
    def create_driver(db: Session, driver_data: DriverCreate):
        db_driver = Driver(**driver_data.dict())
        db.add(db_driver)
        db.commit()
        db.refresh(db_driver)
        return db_driver
  
    def get_drivers(db: Session):
        return db.query(Driver).all()
  
    def get_driver_by_id(db: Session, driver_id: int):
        return db.query(Driver).filter(Driver.id == driver_id).first()
        
    def get_driver_by_email(db: Session, email: str):
        return db.query(Driver).filter(Driver.email == email).first()
        
    def get_driver_by_license(db: Session, license_number: str):
        return db.query(Driver).filter(Driver.license_number == license_number).first()
  
    def update_driver(db: Session, driver_id: int, driver_data: DriverUpdate):
        db_driver = db.query(Driver).filter(Driver.id == driver_id).first()
        if db_driver:
            update_data = driver_data.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_driver, key, value)
            db.commit()
            db.refresh(db_driver)
        return db_driver
  
    def delete_driver(db: Session, driver_id: int):
        db_driver = db.query(Driver).filter(Driver.id == driver_id).first()
        if db_driver:
            db.delete(db_driver)
            db.commit()
        return db_driver
        
    def update_ml_metrics(db: Session, driver_id: int, metrics: Dict[str, Any]):
        """Update machine learning specific metrics for a driver"""
        db_driver = db.query(Driver).filter(Driver.id == driver_id).first()
        if db_driver:
            for key, value in metrics.items():
                if hasattr(db_driver, key):
                    setattr(db_driver, key, value)
            db.commit()
            db.refresh(db_driver)
        return db_driver