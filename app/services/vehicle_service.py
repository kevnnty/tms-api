from sqlalchemy.orm import Session
from app.models.vehicle import Vehicle
from app.schemas.vehicle_schema import VehicleCreate

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

    
    def update_vehicle(db: Session, vehicle_id: int, vehicle_data: VehicleCreate):
        db_vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
        if db_vehicle:
            for key, value in vehicle_data.dict().items():
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
