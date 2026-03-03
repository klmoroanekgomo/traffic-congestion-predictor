"""
Database models for Traffic Congestion System
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, JSON
from sqlalchemy.sql import func
from src.database.database import Base
import uuid

def generate_uuid():
    """Generate UUID for primary keys"""
    return str(uuid.uuid4())

class Route(Base):
    """Routes table"""
    __tablename__ = "routes"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    route_name = Column(String, unique=True, nullable=False, index=True)
    description = Column(String)
    is_active = Column(Boolean, default=True)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Prediction(Base):
    """Predictions table - stores all predictions made"""
    __tablename__ = "predictions"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    route = Column(String, nullable=False, index=True)
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True)
    
    # Input features
    hour = Column(Integer)
    day_of_week = Column(Integer)
    is_weekend = Column(Boolean)
    is_holiday = Column(Boolean)
    month = Column(Integer)
    weather = Column(String)
    temperature = Column(Float)
    
    # Prediction output
    predicted_congestion = Column(Float, nullable=False)
    congestion_level = Column(String)  # Low, Moderate, High
    model_used = Column(String)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

class UserRoute(Base):
    """User's favorite/saved routes"""
    __tablename__ = "user_routes"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, index=True)  # For future user authentication
    route = Column(String, nullable=False)
    nickname = Column(String)  # User's custom name for route
    is_favorite = Column(Boolean, default=False)
    
    # Alert preferences
    alert_threshold = Column(Float)  # Alert when congestion exceeds this
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class PredictionAccuracy(Base):
    """Track prediction accuracy for model monitoring"""
    __tablename__ = "prediction_accuracy"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    route = Column(String, nullable=False, index=True)
    timestamp = Column(DateTime(timezone=True), nullable=False)
    
    predicted_value = Column(Float, nullable=False)
    actual_value = Column(Float)  # To be filled in later with actual data
    error = Column(Float)  # Difference between predicted and actual
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class SystemMetrics(Base):
    """System usage and performance metrics"""
    __tablename__ = "system_metrics"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    
    # Usage metrics
    total_predictions = Column(Integer, default=0)
    api_calls = Column(Integer, default=0)
    unique_routes_queried = Column(Integer, default=0)
    
    # Performance metrics
    avg_response_time_ms = Column(Float)
    model_accuracy = Column(Float)
    
    # Time period
    date = Column(DateTime(timezone=True), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())