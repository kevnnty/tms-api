from fastapi import APIRouter
from pydantic import BaseModel
import pandas as pd
import joblib

router = APIRouter()

# Load models
model = joblib.load('tms_model/models/accident_prediction_model.pkl')
scaler = joblib.load('tms_model/models/scaler.pkl')

feature_columns = [
    'actual_duration', 'expected_duration', 'fuel_consumed', 'actual_distance',
    'average_speed', 'max_speed', 'idle_time', 'driver_fatigue_score'
]

class PredictionRequest(BaseModel):
    actual_duration: float
    expected_duration: float
    fuel_consumed: float
    actual_distance: float
    average_speed: float
    max_speed: float
    idle_time: float
    driver_fatigue_score: float

class PredictionResponse(BaseModel):
    prediction: int
    risk_score: float
    risk_level: str

@router.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    data = pd.DataFrame([request.dict()])
    for col in feature_columns:
        data[col] = data.get(col, 0)
    data = data[feature_columns]

    scaled = scaler.transform(data)
    risk_score = model.predict_proba(scaled)[0][1]
    prediction = int(model.predict(scaled)[0])

    risk_level = (
        "Low" if risk_score < 0.3 else
        "Medium" if risk_score < 0.7 else
        "High"
    )

    return {
        "prediction": prediction,
        "risk_score": float(risk_score),
        "risk_level": risk_level
    }
