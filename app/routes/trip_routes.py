from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional
from datetime import datetime
from app.db.connection import SessionLocal
from app.schemas.trip_schema import TripCreate, TripResponse, TripUpdate
from app.services.trip_service import TripService

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create Trip
@router.post("/", response_model=TripResponse)
def create_trip(trip: TripCreate, db: Session = Depends(get_db)):
    db_trip = TripService.create_trip(db=db, trip_data=trip)
    return db_trip

# List Trips
@router.get("/", response_model=list[TripResponse])
def list_trips(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    trips = TripService.get_trips(db=db, skip=skip, limit=limit)
    return trips

# Get Trip by ID
@router.get("/{trip_id}", response_model=TripResponse)
def get_trip(trip_id: int, db: Session = Depends(get_db)):
    db_trip = TripService.get_trip_by_id(db=db, trip_id=trip_id)
    if db_trip is None:
        raise HTTPException(status_code=404, detail="Trip not found")
    return db_trip

# Get Trips by Driver
@router.get("/driver/{driver_id}", response_model=list[TripResponse])
def get_trips_by_driver(driver_id: int, db: Session = Depends(get_db)):
    trips = TripService.get_trips_by_driver(db=db, driver_id=driver_id)
    return trips

# Get Trips by Vehicle
@router.get("/vehicle/{vehicle_id}", response_model=list[TripResponse])
def get_trips_by_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    trips = TripService.get_trips_by_vehicle(db=db, vehicle_id=vehicle_id)
    return trips

# Get Trips by Route
@router.get("/route/{route_id}", response_model=list[TripResponse])
def get_trips_by_route(route_id: int, db: Session = Depends(get_db)):
    trips = TripService.get_trips_by_route(db=db, route_id=route_id)
    return trips

# Get Trips by Date Range
@router.get("/date-range/", response_model=list[TripResponse])
def get_trips_by_date_range(start_date: datetime, end_date: datetime, db: Session = Depends(get_db)):
    trips = TripService.get_trips_by_date_range(db=db, start_date=start_date, end_date=end_date)
    return trips

# Update Trip
@router.put("/{trip_id}", response_model=TripResponse)
def update_trip(trip_id: int, trip: TripUpdate, db: Session = Depends(get_db)):
    db_trip = TripService.update_trip(db=db, trip_id=trip_id, trip_data=trip)
    if db_trip is None:
        raise HTTPException(status_code=404, detail="Trip not found")
    return db_trip

# Delete Trip
@router.delete("/{trip_id}", response_model=TripResponse)
def delete_trip(trip_id: int, db: Session = Depends(get_db)):
    db_trip = TripService.delete_trip(db=db, trip_id=trip_id)
    if db_trip is None:
        raise HTTPException(status_code=404, detail="Trip not found")
    return db_trip

# Complete Trip
@router.post("/{trip_id}/complete", response_model=TripResponse)
def complete_trip(
    trip_id: int, 
    end_time: datetime,
    end_fuel_level: float,
    actual_distance: float,
    average_speed: float,
    max_speed: float,
    idle_time: float,
    on_time_status: bool = True,
    delay_reason: Optional[str] = None,
    maintenance_issues: Optional[str] = None,
    incidents: Optional[str] = None,
    db: Session = Depends(get_db)
):
    db_trip = TripService.complete_trip(
        db=db, 
        trip_id=trip_id,
        end_time=end_time,
        end_fuel_level=end_fuel_level,
        actual_distance=actual_distance,
        average_speed=average_speed,
        max_speed=max_speed,
        idle_time=idle_time,
        on_time_status=on_time_status,
        delay_reason=delay_reason,
        maintenance_issues=maintenance_issues,
        incidents=incidents
    )
    if db_trip is None:
        raise HTTPException(status_code=404, detail="Trip not found")
    return db_trip

# Get Trip Statistics
@router.get("/statistics/", response_model=Dict[str, Any])
def get_trip_statistics(
    driver_id: Optional[int] = None,
    vehicle_id: Optional[int] = None,
    route_id: Optional[int] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    stats = TripService.get_trip_statistics(
        db=db,
        driver_id=driver_id,
        vehicle_id=vehicle_id,
        route_id=route_id,
        start_date=start_date,
        end_date=end_date
    )
    return stats