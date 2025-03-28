from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any
from app.db.connection import SessionLocal
from app.schemas.route_schema import RouteCreate, RouteResponse, RouteUpdate
from app.services.route_service import RouteService

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create Route
@router.post("/", response_model=RouteResponse)
def create_route(route: RouteCreate, db: Session = Depends(get_db)):
    db_route = RouteService.create_route(db=db, route_data=route)
    return db_route

# List Routes
@router.get("/", response_model=list[RouteResponse])
def list_routes(db: Session = Depends(get_db)):
    routes = RouteService.get_routes(db=db)
    return routes

# Get Route by ID
@router.get("/{route_id}", response_model=RouteResponse)
def get_route(route_id: int, db: Session = Depends(get_db)):
    db_route = RouteService.get_route_by_id(db=db, route_id=route_id)
    if db_route is None:
        raise HTTPException(status_code=404, detail="Route not found")
    return db_route

# Update Route
@router.put("/{route_id}", response_model=RouteResponse)
def update_route(route_id: int, route: RouteUpdate, db: Session = Depends(get_db)):
    db_route = RouteService.update_route(db=db, route_id=route_id, route_data=route)
    if db_route is None:
        raise HTTPException(status_code=404, detail="Route not found")
    return db_route

# Delete Route
@router.delete("/{route_id}", response_model=RouteResponse)
def delete_route(route_id: int, db: Session = Depends(get_db)):
    db_route = RouteService.delete_route(db=db, route_id=route_id)
    if db_route is None:
        raise HTTPException(status_code=404, detail="Route not found")
    return db_route

# Update ML Metrics
@router.patch("/{route_id}/ml-metrics", response_model=RouteResponse)
def update_ml_metrics(route_id: int, metrics: Dict[str, Any], db: Session = Depends(get_db)):
    db_route = RouteService.update_ml_metrics(db=db, route_id=route_id, metrics=metrics)
    if db_route is None:
        raise HTTPException(status_code=404, detail="Route not found")
    return db_route