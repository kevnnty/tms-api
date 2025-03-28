from sqlalchemy.orm import Session
from app.models.trip import Trip
from app.schemas.trip_schema import TripCreate, TripUpdate
from typing import Dict, Any, List, Optional
from datetime import datetime

class TripService:
    def create_trip(db: Session, trip_data: TripCreate):
        db_trip = Trip(**trip_data.dict())
        db.add(db_trip)
        db.commit()
        db.refresh(db_trip)
        return db_trip
  
    def get_trips(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Trip).offset(skip).limit(limit).all()
  
    def get_trip_by_id(db: Session, trip_id: int):
        return db.query(Trip).filter(Trip.id == trip_id).first()
        
    def get_trips_by_driver(db: Session, driver_id: int):
        return db.query(Trip).filter(Trip.driver_id == driver_id).all()
        
    def get_trips_by_vehicle(db: Session, vehicle_id: int):
        return db.query(Trip).filter(Trip.vehicle_id == vehicle_id).all()
        
    def get_trips_by_route(db: Session, route_id: int):
        return db.query(Trip).filter(Trip.route_id == route_id).all()
        
    def get_trips_by_date_range(db: Session, start_date: datetime, end_date: datetime):
        return db.query(Trip).filter(Trip.start_time >= start_date, 
                                    Trip.start_time <= end_date).all()
  
    def update_trip(db: Session, trip_id: int, trip_data: TripUpdate):
        db_trip = db.query(Trip).filter(Trip.id == trip_id).first()
        if db_trip:
            update_data = trip_data.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_trip, key, value)
            db.commit()
            db.refresh(db_trip)
        return db_trip
  
    def delete_trip(db: Session, trip_id: int):
        db_trip = db.query(Trip).filter(Trip.id == trip_id).first()
        if db_trip:
            db.delete(db_trip)
            db.commit()
        return db_trip
        
    def complete_trip(db: Session, trip_id: int, end_time: datetime, 
                     end_fuel_level: float, actual_distance: float,
                     average_speed: float, max_speed: float, idle_time: float,
                     on_time_status: bool = True, delay_reason: Optional[str] = None,
                     maintenance_issues: Optional[str] = None, 
                     incidents: Optional[str] = None):
        """Complete a trip with all the final metrics"""
        db_trip = db.query(Trip).filter(Trip.id == trip_id).first()
        if db_trip:
            db_trip.end_time = end_time
            db_trip.end_fuel_level = end_fuel_level
            db_trip.fuel_consumed = db_trip.start_fuel_level - end_fuel_level
            db_trip.actual_distance = actual_distance
            db_trip.actual_duration = (end_time - db_trip.start_time).total_seconds() / 60  # Convert to minutes
            db_trip.average_speed = average_speed
            db_trip.max_speed = max_speed
            db_trip.idle_time = idle_time
            db_trip.on_time_status = on_time_status
            db_trip.delay_reason = delay_reason
            db_trip.maintenance_issues_reported = maintenance_issues
            db_trip.incidents_reported = incidents
            
            # Update vehicle and driver stats
            if db_trip.vehicle:
                db_trip.vehicle.total_trips += 1
                db_trip.vehicle.total_distance_travelled += actual_distance
            
            if db_trip.driver:
                db_trip.driver.total_trips += 1
                
            db.commit()
            db.refresh(db_trip)
        return db_trip
        
    def get_trip_statistics(db: Session, driver_id: Optional[int] = None, 
                           vehicle_id: Optional[int] = None, 
                           route_id: Optional[int] = None,
                           start_date: Optional[datetime] = None,
                           end_date: Optional[datetime] = None):
        """Get aggregated statistics for trips based on filters"""
        query = db.query(Trip)
        
        if driver_id:
            query = query.filter(Trip.driver_id == driver_id)
        if vehicle_id:
            query = query.filter(Trip.vehicle_id == vehicle_id)
        if route_id:
            query = query.filter(Trip.route_id == route_id)
        if start_date:
            query = query.filter(Trip.start_time >= start_date)
        if end_date:
            query = query.filter(Trip.start_time <= end_date)
            
        trips = query.all()
        
        if not trips:
            return {
                "total_trips": 0,
                "total_distance": 0,
                "total_fuel_consumed": 0,
                "avg_speed": 0,
                "on_time_percentage": 0,
                "avg_idle_time": 0
            }
            
        total_distance = sum(trip.actual_distance for trip in trips if trip.actual_distance)
        total_fuel = sum(trip.fuel_consumed for trip in trips if trip.fuel_consumed)
        total_on_time = sum(1 for trip in trips if trip.on_time_status)
        total_idle_time = sum(trip.idle_time for trip in trips if trip.idle_time)
        avg_speed = sum(trip.average_speed for trip in trips if trip.average_speed) / len(trips) if trips else 0
        
        return {
            "total_trips": len(trips),
            "total_distance": total_distance,
            "total_fuel_consumed": total_fuel,
            "avg_speed": avg_speed,
            "on_time_percentage": (total_on_time / len(trips)) * 100 if trips else 0,
            "avg_idle_time": total_idle_time / len(trips) if trips else 0
        }