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

# Comprehensive Rwanda-specific data
RWANDA_CITIES = [
    "Kigali", "Huye (Butare)", "Rubavu (Gisenyi)", "Musanze (Ruhengeri)", "Muhanga (Gitarama)", 
    "Nyagatare", "Rusizi (Cyangugu)", "Karongi (Kibuye)", "Nyanza", "Rwamagana", "Kayonza", 
    "Gicumbi (Byumba)", "Nyamagabe", "Kirehe", "Kamonyi", "Bugesera", "Gatsibo", "Ngoma", 
    "Nyarugenge", "Gasabo", "Kicukiro"
]

# Rwanda-specific first names
RWANDA_FIRST_NAMES = [
    "Kamanzi", "Mukamana", "Niyonsaba", "Ndagijimana", "Munyaneza", "Iyamuremye", "Umuhoza", 
    "Rwigema", "Uwase", "Mugisha", "Uwimana", "Bizimana", "Hakizimana", "Niyonzima", "Nsengimana", 
    "Niyomugabo", "Habimana", "Nshimiyimana", "Ntawukulilyayo", "Munyakazi", "Niyitegeka", 
    "Murenzi", "Nkurunziza", "Niyibizi", "Nzeyimana", "Munyemana", "Habyarimana", "Nyiraneza", 
    "Mukashema", "Uwineza"
]

# Rwanda-specific last names
RWANDA_LAST_NAMES = [
    "Jean", "Marie", "Pierre", "Claude", "Emmanuel", "Olivier", "Thierry", "Eric", "Patrick", 
    "Innocent", "Jacqueline", "Jeanne", "Odette", "Claudine", "Diane", "Aimable", "Theoneste", 
    "Theogene", "Theophile", "Celestin", "Clementine", "Francois", "Francoise", "Josephine", 
    "Beatrice", "Alphonsine", "Alphonse", "Ignace", "Immaculee", "Esperance"
]

# Rwanda bus companies
RWANDA_BUS_COMPANIES = [
    "Volcano Express", "Ritco Express", "Virunga Express", "Matunda Express", "RFTC", 
    "Horizon Express", "Stella Express", "Royal Express", "Kivu Belt Express", "Alpha Express", 
    "Fidelity Express", "Capital Express", "Sotra Transport", "Kigali Bus Services (KBS)", 
    "Rwanda Inter-Link", "Nyabugogo Transport", "Remera Transport", "Kimironko Express"
]

# Rwanda vehicle models (common in Rwanda)
RWANDA_VEHICLE_MODELS = {
    "Minibus": ["Toyota Hiace", "Toyota Coaster", "Nissan Civilian", "Mitsubishi Rosa"],
    "Bus": ["Yutong ZK6122H9", "Higer KLQ6112", "Golden Dragon XML6127", "Zhongtong LCK6127H"],
    "Truck": ["Isuzu FRR", "Mitsubishi Fuso", "Hino 300 Series", "Mercedes-Benz Actros", "Sinotruk HOWO"],
    "Pickup": ["Toyota Hilux", "Nissan Hardbody", "Isuzu D-Max", "Ford Ranger"],
    "SUV": ["Toyota Land Cruiser", "Toyota RAV4", "Nissan Patrol", "Mitsubishi Pajero"]
}

# Rwanda weather conditions
RWANDA_WEATHER_CONDITIONS = [
    "Clear", "Light Rain", "Heavy Rain", "Foggy", "Cloudy", "Stormy", "Misty"
]

# Rwanda road conditions
RWANDA_ROAD_CONDITIONS = [
    "Good", "Fair", "Poor", "Under Construction", "Washed Out", "Muddy", "Dusty"
]

def random_date(start, end):
    """Generate a random date between start and end"""
    return start + timedelta(
        seconds=random.randint(0, int((end - start).total_seconds()))
    )

def generate_rwandan_license_plate():
    """Generate a realistic Rwandan license plate"""
    plate_types = ["RAA", "RAB", "RAC", "RAD", "RAE", "RAF", "RAG", "IT", "GR", "CD"]
    weights = [0.3, 0.2, 0.2, 0.1, 0.05, 0.05, 0.05, 0.02, 0.02, 0.01]
    
    plate_type = random.choices(plate_types, weights=weights, k=1)[0]
    
    if plate_type in ["IT", "GR", "CD"]:
        return f"{plate_type} {random.randint(1, 999)}"
    else:
        return f"{plate_type} {random.randint(100, 999)} {random.choice('ABCDEFGHJKLM')}"

def generate_rwandan_phone():
    """Generate a realistic Rwandan phone number"""
    prefix = random.choice(["72", "73", "78", "79", "75", "76"])
    return f"+250 {prefix} {random.randint(100, 999)} {random.randint(100, 999)}"

def generate_dataset(num_routes=10, num_vehicles=20, num_drivers=15, num_trips=100):
    """Generate sample data for the TMS database with comprehensive Rwanda-specific data"""
    db = SessionLocal()
    try:
        # Generate Routes with realistic Rwanda locations and distances
        routes = []
        
        # Ensure Kigali is well-represented as a major hub
        kigali_routes = int(num_routes * 0.6)
        other_routes = num_routes - kigali_routes
        
        # Create routes from/to Kigali
        for i in range(1, kigali_routes + 1):
            # Select a non-Kigali destination
            destination = random.choice([city for city in RWANDA_CITIES if "Kigali" not in city])
            
            # Determine if route starts or ends in Kigali
            if random.random() > 0.5:
                start_location = "Kigali"
                end_location = destination
            else:
                start_location = destination
                end_location = "Kigali"
            
            # Calculate realistic distance based on Rwanda's geography
            if "Huye" in destination or "Nyanza" in destination or "Muhanga" in destination:
                distance = random.uniform(80, 140)
            elif "Rubavu" in destination or "Musanze" in destination or "Karongi" in destination:
                distance = random.uniform(100, 180)
            elif "Rwamagana" in destination or "Kayonza" in destination or "Ngoma" in destination:
                distance = random.uniform(40, 100)
            elif "Gicumbi" in destination or "Nyagatare" in destination:
                distance = random.uniform(60, 120)
            else:
                distance = random.uniform(30, 200)
            
            # Calculate realistic travel time (Rwanda's roads average 40-60 km/h)
            avg_speed = random.uniform(40, 60)
            hours = distance / avg_speed
            
            # IMPORTANT: Convert to float for compatibility with old script
            estimated_travel_time = float(hours)
            
            # Calculate realistic cost
            cost_per_km = random.uniform(500, 1500)
            cost = distance * cost_per_km / 1000  # Convert to thousands for compatibility
            
            # Traffic density varies by time of day and route
            avg_traffic_density = 0.8 if "Kigali" in [start_location, end_location] else random.uniform(0.3, 0.6)
            
            # Rwanda has two main seasons: rainy (Mar-May, Oct-Nov) and dry
            seasonal_factors = {
                "winter": random.uniform(0.6, 0.8),  # Mapped to rainy season 1
                "spring": random.uniform(0.7, 0.9),  # Mapped to rainy season 2
                "summer": random.uniform(0.9, 1.0),  # Mapped to dry season 1
                "fall": random.uniform(0.9, 1.0)     # Mapped to dry season 2
            }
            
            # Create time of day efficiency that matches the old format
            time_of_day_efficiency = {str(h): random.uniform(0.7, 1.0) for h in range(24)}
            # Add more realistic values for peak hours
            time_of_day_efficiency.update({
                "7": random.uniform(0.6, 0.7),   # Morning rush
                "8": random.uniform(0.5, 0.6),   # Morning rush peak
                "17": random.uniform(0.5, 0.6),  # Evening rush
                "18": random.uniform(0.6, 0.7),  # Evening rush
            })
            
            route = Route(
                route_code=f"R{i:03d}",  # Match old format
                cost=cost,
                start_location=start_location,
                end_location=end_location,
                estimated_travel_time=estimated_travel_time,  # Now a float
                distance=distance,
                avg_traffic_density=avg_traffic_density,
                avg_fuel_consumption=random.uniform(8, 25),
                historical_delays=random.uniform(10, 45) if avg_traffic_density > 0.6 else random.uniform(5, 20),
                weather_risk_factor=random.uniform(0.3, 0.9),
                time_of_day_efficiency=json.dumps(time_of_day_efficiency),
                day_of_week_efficiency=json.dumps({str(d): random.uniform(0.8, 1.0) for d in range(7)}),
                seasonal_factors=json.dumps(seasonal_factors),
                complexity_score=random.uniform(3, 8) if "Kigali" in [start_location, end_location] else random.uniform(1, 5),
                historical_incidents=random.randint(0, 15) if "Kigali" in [start_location, end_location] else random.randint(0, 8)
            )
            db.add(route)
            routes.append(route)
        
        # Create routes between other cities
        for i in range(kigali_routes + 1, num_routes + 1):
            # Select two different non-Kigali cities
            non_kigali_cities = [city for city in RWANDA_CITIES if "Kigali" not in city]
            cities = random.sample(non_kigali_cities, 2)
            
            # Calculate realistic distance
            distance = random.uniform(20, 150)
            
            # Calculate realistic travel time
            avg_speed = random.uniform(35, 55)
            hours = distance / avg_speed
            estimated_travel_time = float(hours)  # Convert to float for compatibility
            
            # Calculate realistic cost
            cost_per_km = random.uniform(400, 1200)
            cost = distance * cost_per_km / 1000  # Convert to thousands for compatibility
            
            route = Route(
                route_code=f"R{i:03d}",  # Match old format
                cost=cost,
                start_location=cities[0],
                end_location=cities[1],
                estimated_travel_time=estimated_travel_time,
                distance=distance,
                avg_traffic_density=random.uniform(0.2, 0.5),
                avg_fuel_consumption=random.uniform(7, 20),
                historical_delays=random.uniform(5, 30),
                weather_risk_factor=random.uniform(0.4, 0.8),
                time_of_day_efficiency=json.dumps({str(h): random.uniform(0.7, 1.0) for h in range(24)}),
                day_of_week_efficiency=json.dumps({str(d): random.uniform(0.8, 1.0) for d in range(7)}),
                seasonal_factors=json.dumps({
                    "winter": random.uniform(0.6, 0.8),
                    "spring": random.uniform(0.7, 0.9),
                    "summer": random.uniform(0.9, 1.0),
                    "fall": random.uniform(0.9, 1.0)
                }),
                complexity_score=random.uniform(1, 6),
                historical_incidents=random.randint(0, 10)
            )
            db.add(route)
            routes.append(route)
        db.commit()
        
        # Generate Drivers with authentic Rwandan names
        drivers = []
        for i in range(1, num_drivers + 1):
            first_name = random.choice(RWANDA_FIRST_NAMES)
            last_name = random.choice(RWANDA_LAST_NAMES)
            
            # Create realistic Rwandan email
            email_domain = random.choice(["gmail.com", "yahoo.com", "outlook.com", "irembo.rw", "gov.rw"])
            email = f"{first_name.lower()}.{last_name.lower()}{random.randint(1, 999)}@{email_domain}"
            
            # Create realistic Rwandan driver's license
            license_number = f"DL{i:05d}"  # Match old format
            
            # Create certifications in the format expected by the old script
            certifications = ["Basic"]
            if random.random() > 0.4:
                certifications.append("Advanced")
            if random.random() > 0.7:
                certifications.append("Hazardous Materials")
            
            # Create preferred routes in the format expected by the old script
            preferred_routes = random.sample([f"R{r:03d}" for r in range(1, num_routes + 1)], 3)
            
            driver = Driver(
                name=f"{first_name} {last_name}",
                email=email,
                license_number=license_number,
                total_trips=random.randint(10, 200),
                total_earnings=random.uniform(1000, 50000),  # Match old format scale
                safety_score=random.uniform(0.5, 1.0),
                on_time_delivery_rate=random.uniform(0.7, 1.0),
                experience_years=random.uniform(0.5, 15),
                rest_compliance_rate=random.uniform(0.7, 1.0),
                avg_speed_profile=json.dumps({
                    "highway": random.uniform(50, 70),
                    "city": random.uniform(15, 30),
                    "residential": random.uniform(30, 50)  # Use "residential" instead of "rural" for compatibility
                }),
                harsh_braking_events=random.randint(0, 50),
                harsh_acceleration_events=random.randint(0, 40),
                fuel_efficiency_score=random.uniform(0.6, 1.0),
                route_adherence=random.uniform(0.7, 1.0),
                customer_satisfaction=random.uniform(3.0, 5.0),
                training_level=random.randint(1, 5),
                certifications=json.dumps(certifications),
                preferred_routes=json.dumps(preferred_routes),
                fatigue_score=random.uniform(0.1, 0.5)
            )
            db.add(driver)
            drivers.append(driver)
        db.commit()
        
        # Generate Vehicles common in Rwanda
        available_drivers = drivers.copy()
        random.shuffle(available_drivers)
        
        vehicles = []
        for i in range(1, num_vehicles + 1):
            # Determine vehicle type distribution
            vehicle_type = random.choices(
                ["Minibus", "Bus", "Truck", "Pickup", "SUV"],
                weights=[0.4, 0.2, 0.25, 0.1, 0.05],
                k=1
            )[0]
            
            # Set model based on vehicle type
            model = random.choice(RWANDA_VEHICLE_MODELS[vehicle_type])
            
            # Set capacity based on vehicle type
            if vehicle_type == "Minibus":
                capacity = random.randint(14, 18)
                category = "Coaster"  # Match old format
            elif vehicle_type == "Bus":
                capacity = random.randint(25, 60)
                category = "Coach"  # Match old format
            elif vehicle_type == "Truck":
                capacity = random.randint(50, 100)  # Match old format scale
                category = "Cab"  # Match old format
            elif vehicle_type == "Pickup":
                capacity = random.randint(29, 50)  # Match old format scale
                category = "Coaster"  # Match old format
            else:  # SUV
                capacity = random.randint(29, 50)  # Match old format scale
                category = "Coaster"  # Match old format
            
            # Rwanda vehicles are often older
            manufacture_year = random.randint(2010, 2023)  # Match old format range
            
            # Assign a driver if available
            assign_driver = random.random() > 0.2 and available_drivers
            
            # Generate realistic Rwandan license plate
            license_plate = f"VEH{i:04d}"  # Match old format
            
            # Assign a bus company for passenger vehicles
            company_name = random.choice(RWANDA_BUS_COMPANIES) if vehicle_type in ["Minibus", "Bus"] else None
            
            vehicle = Vehicle(
                license_plate=license_plate,
                model=model,
                capacity=capacity,
                category=category,
                status=random.choice(["active", "maintenance", "inactive"]),
                total_trips=random.randint(10, 300),
                total_distance_travelled=random.uniform(1000, 100000),  # Match old format scale
                manufacture_year=manufacture_year,
                fuel_efficiency=random.uniform(5, 20),  # Match old format scale
                maintenance_score=random.uniform(0.5, 0.9),
                last_maintenance_date=(datetime.now() - timedelta(days=random.randint(1, 180))).strftime("%Y-%m-%d"),
                maintenance_frequency=random.randint(30, 180),  # Match old format range
                engine_hours=random.uniform(1000, 20000),  # Match old format scale
                idle_time_percentage=random.uniform(0.05, 0.3),  # Match old format range
                avg_speed=random.uniform(30, 60),  # Match old format range
                emissions_data=json.dumps({"co2": random.uniform(100, 300), "nox": random.uniform(10, 50)}),  # Match old format
                tire_wear_rate=random.uniform(0.001, 0.01),  # Match old format range
                breakdown_frequency=random.uniform(0.001, 0.05),  # Match old format range
                sensor_data_json=json.dumps({
                    "engine_temp": random.uniform(180, 220),
                    "oil_pressure": random.uniform(30, 70),
                    "battery": random.uniform(12, 14)
                }),  # Match old format
                operational_cost_per_mile=random.uniform(0.5, 2.0),  # Match old format range
                driver_id=available_drivers.pop().id if assign_driver else None,
                route_id=random.choice(routes).id if random.random() > 0.3 else None,
                company_name=company_name
            )
            db.add(vehicle)
            vehicles.append(vehicle)
        db.commit()
        
        # Generate Trips
        start_date = datetime.now() - timedelta(days=365)
        
        # Create a mapping of driver_id to vehicle_id for trip assignment
        driver_vehicle_map = {}
        for vehicle in vehicles:
            if vehicle.driver_id:
                driver_vehicle_map[vehicle.driver_id] = vehicle.id
        
        for i in range(1, num_trips + 1):
            # First select a random driver
            driver = random.choice(drivers)
            
            # If driver has an assigned vehicle, use that vehicle
            if driver.id in driver_vehicle_map:
                vehicle_id = driver_vehicle_map[driver.id]
            else:
                # If driver doesn't have a vehicle, select a vehicle without a driver
                unassigned_vehicles = [v for v in vehicles if v.driver_id is None]
                if unassigned_vehicles:
                    vehicle_id = random.choice(unassigned_vehicles).id
                else:
                    # If all vehicles have drivers, just pick a random one
                    vehicle_id = random.choice(vehicles).id
            
            route = random.choice(routes)
            
            # Generate trip start time - weighted toward business hours
            hour_weights = [0.01, 0.01, 0.01, 0.02, 0.05, 0.08, 0.1, 0.1, 0.1, 0.08, 
                           0.06, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.04, 
                           0.03, 0.02, 0.02, 0.01, 0.01]
            
            # Generate random date
            random_day = random_date(start_date, datetime.now())
            
            # If it's Sunday, 70% chance to regenerate (less trips on Sunday)
            if random_day.weekday() == 6 and random.random() < 0.7:
                random_day = random_date(start_date, datetime.now())
            
            # Generate random hour based on weights
            random_hour = random.choices(range(24), weights=hour_weights, k=1)[0]
            
            # Set the time
            trip_start = random_day.replace(hour=random_hour, minute=random.randint(0, 59))
            
            # Calculate expected duration in minutes from route
            expected_duration = float(route.estimated_travel_time) * 60  # Convert hours to minutes
            
            # Determine if trip is completed
            is_completed = random.random() > 0.2  # 80% completion rate
            
            # Adjust cargo type based on vehicle category
            cargo_type = random.choice(["General", "Perishable", "Fragile"])  # Match old format
            
            # Create trip with required fields
            trip = Trip(
                vehicle_id=vehicle_id,
                driver_id=driver.id,
                route_id=route.id,
                start_time=trip_start,
                expected_duration=expected_duration,
                planned_distance=route.distance,
                start_fuel_level=random.uniform(50, 100),
                weather_conditions=random.choice(["Clear", "Rain", "Fog"]),  # Match old format
                traffic_conditions=random.choice(["Light", "Moderate", "Heavy"]),
                cargo_weight=random.uniform(500, 8000),  # Match old format scale
                cargo_type=cargo_type,
                driver_fatigue_score=random.uniform(0.1, 0.7)
            )
            
            # Add completed trip data if applicable
            if is_completed:
                # Calculate actual duration as a variation of expected
                variation_factor = random.uniform(0.8, 1.2)
                actual_duration = expected_duration * variation_factor
                
                # Set end time based on start time and actual duration
                trip.end_time = trip_start + timedelta(minutes=actual_duration)
                trip.actual_duration = actual_duration
                
                # Calculate fuel consumption
                trip.end_fuel_level = trip.start_fuel_level - random.uniform(10, 40)  # Match old format
                trip.fuel_consumed = trip.start_fuel_level - trip.end_fuel_level
                
                # Set distance and speed metrics
                trip.actual_distance = route.distance * random.uniform(0.95, 1.1)  # Match old format
                trip.average_speed = trip.actual_distance / (actual_duration / 60)  # km/h
                trip.max_speed = trip.average_speed * random.uniform(1.1, 1.5)  # Match old format
                trip.idle_time = actual_duration * random.uniform(0.05, 0.2)  # Match old format
                
                # Determine if trip was on time
                trip.on_time_status = actual_duration <= expected_duration * 1.1  # Match old format
                
                # Add delay reason if applicable
                if not trip.on_time_status:
                    trip.delay_reason = random.choice([
                        "Traffic congestion", "Weather conditions", "Vehicle breakdown",
                        "Driver rest period", "Loading/unloading delay"
                    ])  # Match old format
                
                # Randomly add maintenance issues
                if random.random() < 0.1:  # Match old format probability
                    trip.maintenance_issues_reported = random.choice([
                        "Check engine light", "Brake noise", "Transmission issues", "Tire pressure warning"
                    ])  # Match old format
                
                # Randomly add incidents
                if random.random() < 0.05:  # Match old format probability
                    trip.incidents_reported = random.choice([
                        "Minor collision", "Cargo shift", "Road closure detour", "Mechanical failure"
                    ])  # Match old format
            
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