import random
import json
import uuid
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.route import Route
from app.models.vehicle import Vehicle
from app.models.driver import Driver
from app.models.trip import Trip
from app.db.connection import SessionLocal

# Common Rwandan Locations
locations = [
    "Kigali", "Butare", "Gisenyi", "Musanze", "Nyundo", "Rubavu", "Nyanza", "Rwamagana",
    "Kibuye", "Gicumbi", "Kayonza", "Huye", "Karongi", "Nyamagabe", "Kirehe", "Kamonyi"
]

# Common Rwandan Driver Names (First & Last)
first_names = [
    "Kamanzi", "Mukamana", "Niyonsaba", "Ndagijimana", "Munyaneza", "Iyamuremye", "Umuhoza", 
    "Rwigema", "Uwase", "Mugisha"
]

last_names = [
    "John", "Alice", "Jacqueline", "Emmanuel", "Jean", "Odette", "Eric", "Thierry", "Anitha", "Claude"
]

def random_date(start, end):
    """Generate a random date between start and end"""
    return start + timedelta(
        seconds=random.randint(0, int((end - start).total_seconds()))
    )

def generate_dataset(num_routes=10, num_vehicles=20, num_drivers=15, num_trips=100):
    """Generate sample data for the TMS database with Rwanda-specific data"""
    db = SessionLocal()
    try:
        # Generate Routes
        routes = []
        for i in range(1, num_routes + 1):
            route = Route(
                route_code=f"R{i:03d}",
                cost=random.uniform(100, 500),
                start_location=random.choice(locations),
                end_location=random.choice(locations),
                estimated_travel_time=random.randint(1, 10),
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
        
        # Generate Drivers with Rwandan names
        drivers = []
        for i in range(1, num_drivers + 1):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            driver = Driver(
                name=f"{first_name} {last_name}",
                email=f"driver{uuid.uuid4().hex[:8]}@example.com",  # Ensure unique emails
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
                preferred_routes=json.dumps(random.sample([f"R{r:03d}" for r in range(1, num_routes + 1)], 3)),
                fatigue_score=random.uniform(0.1, 0.5)
            )
            db.add(driver)
            drivers.append(driver)
        db.commit()
        
        # Generate Vehicles with Rwanda-relevant types
        available_drivers = drivers.copy()
        random.shuffle(available_drivers)  # Shuffle to randomize assignment
        
        vehicles = []
        for i in range(1, num_vehicles + 1):
            # Determine if this vehicle should have a driver
            assign_driver = random.random() > 0.2 and available_drivers
            
            vehicle = Vehicle(
                license_plate=f"VEH{i:04d}",
                model=random.choice(["Toyota Hilux", "Toyota Land Cruiser", "Nissan Patrol", "Isuzu D-Max", "YuTong"]),
                capacity=random.randint(29, 100),
                category=random.choice(["Coaster", "Coach", "Cab"]),
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
                emissions_data=json.dumps({"co2": random.uniform(100, 300), "nox": random.uniform(10, 50)}),
                tire_wear_rate=random.uniform(0.001, 0.01),
                breakdown_frequency=random.uniform(0.001, 0.05),
                sensor_data_json=json.dumps({"engine_temp": random.uniform(180, 220),
                                            "oil_pressure": random.uniform(30, 70),
                                            "battery": random.uniform(12, 14)}),
                operational_cost_per_mile=random.uniform(0.5, 2.0),
                driver_id=available_drivers.pop().id if assign_driver else None,
                route_id=random.choice(routes).id if random.random() > 0.3 else None,
                company_name=random.choice(["Volcano Express", "Ritco Express", "Matunda Express", "RFTC Express", "Yahoo Express", "Stella Express", "Star Express", "Kivu Belt Express", "International Express", "Horizon Express", "Fidelity Express", "Capital Express", "Alpha Express"])
            )

            db.add(vehicle)
            vehicles.append(vehicle)
        db.commit()
        
        # Generate Trips
        start_date = datetime.now() - timedelta(days=365)
        
        driver_vehicle_map = {}
        for vehicle in vehicles:
            if vehicle.driver_id:
                driver_vehicle_map[vehicle.driver_id] = vehicle.id
        
        for i in range(1, num_trips + 1):
            driver = random.choice(drivers)
            
            if driver.id in driver_vehicle_map:
                vehicle_id = driver_vehicle_map[driver.id]
            else:
                unassigned_vehicles = [v for v in vehicles if v.driver_id is None]
                if unassigned_vehicles:
                    vehicle_id = random.choice(unassigned_vehicles).id
                else:
                    vehicle_id = random.choice(vehicles).id
            
            route = random.choice(routes)
            
            trip_start = random_date(start_date, datetime.now())
            
            expected_duration = float(route.estimated_travel_time) * 60  # Convert hours to minutes
            
            is_completed = random.random() > 0.2
            
            trip = Trip(
                vehicle_id=vehicle_id,
                driver_id=driver.id,
                route_id=route.id,
                start_time=trip_start,
                expected_duration=expected_duration,
                planned_distance=route.distance,
                start_fuel_level=random.uniform(50, 100),
                weather_conditions=random.choice(["Clear", "Rain", "Fog"]),
                traffic_conditions=random.choice(["Light", "Moderate", "Heavy"]),
                cargo_weight=random.uniform(500, 8000),
                cargo_type=random.choice(["General", "Perishable", "Fragile"]),
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
                        "Traffic congestion", "Weather conditions", "Vehicle breakdown",
                        "Driver rest period", "Loading/unloading delay"
                    ])
                if random.random() < 0.1:
                    trip.maintenance_issues_reported = random.choice([
                        "Check engine light", "Brake noise", "Transmission issues", "Tire pressure warning"
                    ])
                if random.random() < 0.05:
                    trip.incidents_reported = random.choice([
                        "Minor collision", "Cargo shift", "Road closure detour", "Mechanical failure"
                    ])
            
            db.add(trip)
            
            if i % 100 == 0:
                db.commit()
        
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
        return {"error": str(e), "details": str(type(e))}
    finally:
        db.close()
