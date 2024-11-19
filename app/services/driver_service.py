from sqlalchemy.orm import Session
from app.models.driver import Driver
from app.schemas.driver_schema import DriverCreate

class DriverService:
    
    
    def create_driver(db: Session, driver_data: DriverCreate):
        db_driver = Driver(**driver_data.dict())
        db.add(db_driver)
        db.commit()
        db.refresh(db_driver)
        return db_driver

    
    
    def get_drivers(db: Session, skip: int = 0, limit: int = 10):
        return db.query(Driver).offset(skip).limit(limit).all()

    
    
    def get_driver_by_id(db: Session, driver_id: int):
        return db.query(Driver).filter(Driver.id == driver_id).first()

    
    
    def update_driver(db: Session, driver_id: int, driver_data: DriverCreate):
        db_driver = db.query(Driver).filter(Driver.id == driver_id).first()
        if db_driver:
            for key, value in driver_data.dict().items():
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
