from sqlalchemy.orm import Session
from app.models.vehicle import Vehicle
from app.schemas.vehicle import VehicleCreate

def create_vehicle_service(vehicle_data: VehicleCreate, db: Session) -> Vehicle:
    """Create a new vehicle."""
    db_vehicle = Vehicle(**vehicle_data.dict())
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle

def list_vehicles_service(skip: int, limit: int, db: Session) -> list[Vehicle]:
    """Fetch a list of vehicles with pagination."""
    return db.query(Vehicle).offset(skip).limit(limit).all()
