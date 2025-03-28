import random
import json
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.route import Route
from app.models.vehicle import Vehicle
from app.models.driver import Driver
from app.models.trip import Trip
from app.db.connection import SessionLocal

def generate_sample_data(num_routes=10, num_vehicles=20, num_drivers=15, num_trips=100):
    """Generate sample data for the TMS database"""
    db = SessionLocal()
    try:
        # Generate Routes
        routes = []
        for i in range(1, num_routes + 1):
            route = Route(
                route_code=f"R{i:03d}",
                cost=random.uniform(100, 500),
                start_location=f"Location {random.randint(1, 50)}",
                end_location=f"Location {random.randint(1, 50)}",
                estimated_travel_time=f"{random.randint(1, 10)} hours",
                distance=random.uniform(50, 500),
                avg_traffic_density=random.uniform(0.1, 0.9),
                avg_fuel_consumption=random.uniform(10, 30),
                historical_delays=random.uniform(0, 60),
                weather_risk_factor=random.uniform(0.1, 0.8),
                time_of_day_efficiency=json.dumps({str(h): random.uniform(0.7, 1.0) for h in range(24)}),
                day_of_week_efficiency=json.dumps({str(d): random.uniform(0.8, 1.0) for d in range(7)}),
                seasonal_factors=json.dumps({"winter": random.uniform(0.7, 0.9), 
                                           "spring": random.uniform(0.8, 1.0),
                                           "summer": random.uniform(0.9, 1.0),
                                           "fall": random.uniform(0.8, 0.95)}),
                complexity_score=random.uniform(1, 10),
                historical_incidents=random.randint(0, 20)
            )
            db.add(route)
            routes.append(route)
        db.commit()
        
        # Generate Drivers
        drivers = []
        for i in range(1, num_drivers + 1):
            driver = Driver(
                name=f"Driver {i}",
                email=f"driver{i}@example.com",
                license_number=f"DL{i:05d}",
                total_trips=random.randint(10, 200),
                total_earnings=random.uniform(1000, 50000),
                safety_score=random.uniform(0.5, 1.0),
                on_time_delivery_rate=random.uniform(0.7, 1.0),
                experience_years=random.uniform(0.5, 20),
                rest_compliance_rate=random.uniform(0.7, 1.0),
                avg_speed_profile=json.dumps({"highway": random.uniform(55, 75), 
                                            "city": random.uniform(20, 35),
                                            "residential": random.uniform(15, 25)}),
                harsh_braking_events=random.randint(0, 50),
                harsh_acceleration_events=random.randint(0, 40),
                fuel_efficiency_score=random.uniform(0.6, 1.0),
                route_adherence=random.uniform(0.7, 1.0),
                customer_satisfaction=random.uniform(3.0, 5.0),
                training_level=random.randint(1, 5),
                certifications=json.dumps(["Basic", "Advanced"] if random.random() > 0.5 else ["Basic"]),
                preferred_routes=json.dumps([f"R{random.randint(1, num_routes):03d}" for _ in range(3)]),
                fatigue_score=random.uniform(0.1, 0.5)
            )
            db.add(driver)
            drivers.append(driver)
        db.commit()
        
        # Generate Vehicles
        vehicles = []
        for i in range(1, num_vehicles + 1):
            vehicle = Vehicle(
                license_plate=f"VEH{i:04d}",
                model=random.choice(["Model A", "Model B", "Model C", "Model D"]),
                capacity=random.randint(1000, 10000),
                category=random.choice(["Light", "Medium", "Heavy"]),
                status=random.choice(["active", "maintenance", "inactive"]),
                total_trips=random.randint(10, 300),
                total_distance_travelled=random.uniform(1000, 100000),
                manufacture_year=random.randint(2010, 2023),
                fuel_efficiency=random.uniform(5, 20),
                maintenance_score=random.uniform(0.5, 1.0),
                last_maintenance_date=(datetime.now() - timedelta(days=random.randint(1, 180))).strftime("%Y-%m-%d"),
                maintenance_frequency=random.randint(30, 180),
                engine_hours=random.uniform(1000, 20000),
                idle_time_percentage=random.uniform(0.05, 0.3),
                avg_speed=random.uniform(30, 60),
                emissions_data=json.dumps({"co2": random.uniform(100, 300), 
                                         "nox": random.uniform(10, 50)}),
                tire_wear_rate=random.uniform(0.001, 0.01),
                breakdown_frequency=random.uniform(0.001, 0.05),
                sensor_data_json=json.dumps({"engine_temp": random.uniform(180, 220),
                                           "oil_pressure": random.uniform(30, 70),
                                           "battery": random.uniform(12, 14)}),
                operational_cost_per_mile=random.uniform(0.5, 2.0),
                driver_id=random.choice(drivers).id if random.random() > 0.2 else None,
                route_id=random.choice(routes).id if random.random() > 0.3 else None
            )
            db.add(vehicle)
            vehicles.append(vehicle)
        db.commit()
        
        # Generate Trips
        start_date = datetime.now() - timedelta(days=365)
        for i in range(1, num_trips + 1):
            vehicle = random.choice(vehicles)
            driver = random.choice(drivers)
            route = random.choice(routes)
            
            trip_start = start_date + timedelta(days=random.randint(1, 364))
            expected_duration = float(route.estimated_travel_time.split()[0]) * 60  # Convert to minutes
            
            # Some trips are completed, some are in progress
            is_completed = random.random() > 0.2
            
            trip = Trip(
                vehicle_id=vehicle.id,
                driver_id=driver.id,
                route_id=route.id,
                start_time=trip_start,
                expected_duration=expected_duration,
                planned_distance=route.distance,
                start_fuel_level=random.uniform(50, 100),
                weather_conditions=random.choice(["Clear", "Rain", "Snow", "Fog", "Windy"]),
                traffic_conditions=random.choice(["Light", "Moderate", "Heavy"]),
                cargo_weight=random.uniform(500, 8000),
                cargo_type=random.choice(["General", "Perishable", "Hazardous", "Fragile"]),
                driver_fatigue_score=random.uniform(0.1, 0.7)
            )
            
            if is_completed:
                actual_duration = expected_duration * random.uniform(0.8, 1.2)
                trip.end_time = trip_start + timedelta(minutes=actual_duration)
                trip.actual_duration = actual_duration
                trip.end_fuel_level = trip.start_fuel_level - random.uniform(10, 40)
                trip.fuel_consumed = trip.start_fuel_level - trip.end_fuel_level
                trip.actual_distance = route.distance * random.uniform(0.95, 1.1)
                trip.average_speed = trip.actual_distance / (actual_duration / 60)
                trip.max_speed = trip.average_speed * random.uniform(1.1, 1.5)
                trip.idle_time = actual_duration * random.uniform(0.05, 0.2)
                trip.on_time_status = actual_duration <= expected_duration * 1.1
                
                if not trip.on_time_status:
                    trip.delay_reason = random.choice([
                        "Traffic congestion", 
                        "Weather conditions", 
                        "Vehicle breakdown", 
                        "Driver rest period", 
                        "Loading/unloading delay"
                    ])
                
                if random.random() < 0.1:
                    trip.maintenance_issues_reported = random.choice([
                        "Check engine light", 
                        "Brake noise", 
                        "Transmission issues", 
                        "Tire pressure warning"
                    ])
                
                if random.random() < 0.05:
                    trip.incidents_reported = random.choice([
                        "Minor collision", 
                        "Cargo shift", 
                        "Road closure detour", 
                        "Mechanical failure"
                    ])
            
            db.add(trip)
        
        db.commit()
        return {
            "routes": num_routes,
            "vehicles": num_vehicles,
            "drivers": num_drivers,
            "trips": num_trips,
            "status": "Data generated successfully"
        }
    
    except Exception as e:
        db.rollback()
        return {"error": str(e)}
    finally:
        db.close()
