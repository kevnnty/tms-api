import requests
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

# FastAPI Server Base URL
BASE_URL = "http://localhost:5000"

# Fetch routes
def fetch_routes():
    response = requests.get(f"{BASE_URL}/routes")
    return response.json() if response.status_code == 200 else []

# Fetch vehicles
def fetch_vehicles():
    response = requests.get(f"{BASE_URL}/vehicles")
    return response.json() if response.status_code == 200 else []

# Fetch drivers
def fetch_drivers():
    response = requests.get(f"{BASE_URL}/drivers")
    return response.json() if response.status_code == 200 else []

# Load data
def load_data():
    routes = fetch_routes()
    vehicles = fetch_vehicles()
    drivers = fetch_drivers()
    
    data = []
    for route in routes:
        vehicle = next((v for v in vehicles if v['id'] == route['vehicle_id']), None)
        driver = next((d for d in drivers if d['id'] == route['driver_id']), None)
        
        if vehicle and driver:
            data.append({
                "distance": route["distance"],
                "avg_speed": vehicle["avg_speed"],
                "traffic_condition": route["traffic_condition"],
                "driver_experience": driver["years_of_experience"],
                "actual_eta": route["actual_eta"]
            })
    
    return pd.DataFrame(data)

# Train Model
def train_model():
    df = load_data()
    X = df.drop(columns=["actual_eta"])
    y = df["actual_eta"]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    print(f"Model trained with MAE: {mae}")
    
    return model

if __name__ == "__main__":
    model = train_model()
