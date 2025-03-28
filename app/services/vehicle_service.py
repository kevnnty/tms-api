from sqlalchemy.orm import Session
from app.models.vehicle import Vehicle
from app.schemas.vehicle_schema import VehicleCreate, VehicleUpdate
from typing import Dict, Any

class VehicleService:
    def create_vehicle(db: Session, vehicle_data: VehicleCreate):
        db_vehicle = Vehicle(**vehicle_data.dict())
        db.add(db_vehicle)
        db.commit()
        db.refresh(db_vehicle)
        return db_vehicle
  
    def get_vehicles(db: Session):
        return db.query(Vehicle).all()
  
    def get_vehicle_by_id(db: Session, vehicle_id: int):
        return db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
        
    def get_vehicle_by_license_plate(db: Session, license_plate: str):
        return db.query(Vehicle).filter(Vehicle.license_plate == license_plate).first()
  
    def update_vehicle(db: Session, vehicle_id: int, vehicle_data: VehicleUpdate):
        db_vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
        if db_vehicle:
            update_data = vehicle_data.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_vehicle, key, value)
            db.commit()
            db.refresh(db_vehicle)
        return db_vehicle
  
    def delete_vehicle(db: Session, vehicle_id: int):
        db_vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
        if db_vehicle:
            db.delete(db_vehicle)
            db.commit()
        return db_vehicle
        
    def update_ml_metrics(db: Session, vehicle_id: int, metrics: Dict[str, Any]):
        """Update machine learning specific metrics for a vehicle"""
        db_vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
        if db_vehicle:
            for key, value in metrics.items():
                if hasattr(db_vehicle, key):
                    setattr(db_vehicle, key, value)
            db.commit()
            db.refresh(db_vehicle)
        return db_vehicle