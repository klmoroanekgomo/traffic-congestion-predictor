"""
FastAPI application for traffic congestion prediction
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
import pandas as pd
import joblib
import numpy as np
from datetime import datetime
from contextlib import asynccontextmanager
import sys
import os

# Get the project root directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(PROJECT_ROOT, 'src'))

from data_processing.feature_engineering import FeatureEngineer

# Global variables for model
model = None
model_info = None
feature_engineer = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load the trained model and encoders on startup"""
    global model, model_info, feature_engineer
    
    try:
        model_path = os.path.join(PROJECT_ROOT, 'models', 'best_model.pkl')
        model_info_path = os.path.join(PROJECT_ROOT, 'models', 'model_info.pkl')
        encoders_path = os.path.join(PROJECT_ROOT, 'models', 'label_encoders.pkl')
        
        model = joblib.load(model_path)
        model_info = joblib.load(model_info_path)
        
        feature_engineer = FeatureEngineer()
        feature_engineer.load_encoders(encoders_path)
        
        print("✓ Model and encoders loaded successfully")
        print(f"  Model: {model_info['model_name']}")
        print(f"  Validation R²: {model_info['metrics']['val_r2']:.4f}")
        print(f"  Trained on: {model_info['training_date']}")
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        raise
    
    yield
    
    # Cleanup (if needed)
    print("Shutting down...")

# Initialize FastAPI app with lifespan
app = FastAPI(
    title="Traffic Congestion Prediction API",
    description="Predict traffic congestion levels for Johannesburg routes",
    version="1.0.0",
    lifespan=lifespan
)

# Pydantic models for request/response validation
class PredictionRequest(BaseModel):
    """Request model for single prediction"""
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "timestamp": "2024-06-15 08:30:00",
            "route": "M1_North",
            "weather": "Clear",
            "temperature": 18.5,
            "is_holiday": False
        }
    })
    
    timestamp: str
    route: str
    weather: str
    temperature: float
    is_holiday: bool = False

class PredictionResponse(BaseModel):
    """Response model for prediction"""
    congestion_score: float
    congestion_level: str
    timestamp: str
    route: str
    weather: str
    model_used: str
    confidence: str

class BatchPredictionRequest(BaseModel):
    """Request model for batch predictions"""
    predictions: List[PredictionRequest]

class ModelInfoResponse(BaseModel):
    """Response model for model information"""
    model_name: str
    training_date: str
    n_features: int
    n_samples: int
    metrics: dict

# API Endpoints
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Traffic Congestion Prediction API",
        "version": "1.0.0",
        "status": "active",
        "endpoints": {
            "predict": "/predict",
            "batch_predict": "/batch-predict",
            "model_info": "/model/info",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/model/info", response_model=ModelInfoResponse)
async def get_model_info():
    """Get information about the loaded model"""
    if model_info is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    return model_info

@app.post("/predict", response_model=PredictionResponse)
async def predict_congestion(request: PredictionRequest):
    """
    Predict traffic congestion for a single request
    
    Parameters:
    - timestamp: Date and time in format "YYYY-MM-DD HH:MM:SS"
    - route: Route name (e.g., M1_North, N1_South, etc.)
    - weather: Weather condition (Clear, Rain, Cloudy, Drizzle)
    - temperature: Temperature in Celsius
    - is_holiday: Whether it's a public holiday
    """
    
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    try:
        # Create dataframe from request
        data = {
            'timestamp': [request.timestamp],
            'route': [request.route],
            'weather': [request.weather],
            'temperature': [request.temperature],
            'is_holiday': [request.is_holiday],
            'is_weekend': [False],  # Will be calculated from timestamp
            'congestion_score': [0],  # Placeholder
            'avg_speed_kmh': [0],  # Placeholder
            'traffic_volume': [0]  # Placeholder
        }
        
        df = pd.DataFrame(data)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Extract day name
        df['day_name'] = df['timestamp'].dt.day_name()
        df['is_weekend'] = df['timestamp'].dt.dayofweek >= 5
        
        # Engineer features
        df = feature_engineer.create_features(df)
        
        # Encode categorical variables
        categorical_cols = ['route', 'weather', 'day_name', 'time_of_day']
        df = feature_engineer.encode_categorical(df, categorical_cols, fit=False)
        
        # Prepare features (same order as training)
        exclude_cols = ['timestamp', 'congestion_level', 'congestion_score',
                       'route', 'weather', 'day_name', 'time_of_day']
        feature_cols = [col for col in df.columns if col not in exclude_cols]
        
        X = df[feature_cols]
        
        # Make prediction
        prediction = model.predict(X)[0]
        
        # Classify congestion level
        if prediction < 30:
            congestion_level = "Low"
            confidence = "High"
        elif prediction < 60:
            congestion_level = "Moderate"
            confidence = "High"
        else:
            congestion_level = "High"
            confidence = "High"
        
        return PredictionResponse(
            congestion_score=round(float(prediction), 2),
            congestion_level=congestion_level,
            timestamp=request.timestamp,
            route=request.route,
            weather=request.weather,
            model_used=model_info['model_name'],
            confidence=confidence
        )
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction error: {str(e)}")

@app.post("/batch-predict")
async def batch_predict_congestion(request: BatchPredictionRequest):
    """
    Predict traffic congestion for multiple requests
    """
    
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    try:
        results = []
        
        for pred_request in request.predictions:
            result = await predict_congestion(pred_request)
            results.append(result.dict())
        
        return {
            "predictions": results,
            "count": len(results),
            "model_used": model_info['model_name']
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Batch prediction error: {str(e)}")

@app.get("/routes")
async def get_available_routes():
    """Get list of available routes"""
    routes = [
        'M1_North', 'M1_South', 'N1_North', 'N1_South',
        'N3_East', 'N3_West', 'M2_East', 'M2_West',
        'William_Nicol', 'Rivonia_Road', 'Jan_Smuts',
        'Sandton_Drive', 'Pretoria_Main', 'Soweto_Highway'
    ]
    
    return {
        "routes": routes,
        "count": len(routes)
    }

@app.get("/weather-conditions")
async def get_weather_conditions():
    """Get list of valid weather conditions"""
    weather_conditions = ['Clear', 'Rain', 'Cloudy', 'Drizzle']
    
    return {
        "weather_conditions": weather_conditions,
        "count": len(weather_conditions)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)