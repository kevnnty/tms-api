from sqlalchemy.orm import Session
from app.models.route import Route
from app.schemas.route_schema import RouteCreate, RouteUpdate
from typing import Dict, Any

class RouteService:
    def create_route(db: Session, route_data: RouteCreate):
        db_route = Route(**route_data.dict())
        db.add(db_route)
        db.commit()
        db.refresh(db_route)
        return db_route
  
    def get_routes(db: Session):
        return db.query(Route).all()
  
    def get_route_by_id(db: Session, route_id: int):
        return db.query(Route).filter(Route.id == route_id).first()
  
    def update_route(db: Session, route_id: int, route_data: RouteUpdate):
        db_route = db.query(Route).filter(Route.id == route_id).first()
        if db_route:
            update_data = route_data.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_route, key, value)
            db.commit()
            db.refresh(db_route)
        return db_route
  
    def delete_route(db: Session, route_id: int):
        db_route = db.query(Route).filter(Route.id == route_id).first()
        if db_route:
            db.delete(db_route)
            db.commit()
        return db_route
        
    def update_ml_metrics(db: Session, route_id: int, metrics: Dict[str, Any]):
        """Update machine learning specific metrics for a route"""
        db_route = db.query(Route).filter(Route.id == route_id).first()
        if db_route:
            for key, value in metrics.items():
                if hasattr(db_route, key):
                    setattr(db_route, key, value)
            db.commit()
            db.refresh(db_route)
        return db_route