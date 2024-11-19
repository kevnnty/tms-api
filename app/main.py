from fastapi import FastAPI
from app.routes import vehicle_routes
from app.db.connection import engine, Base

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(vehicle_routes.router)
