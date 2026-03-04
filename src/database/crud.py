"""
CRUD operations for Traffic Congestion database
"""

from sqlalchemy.orm import Session
from sqlalchemy import select, func, desc
from src.database.models import Route, Prediction, UserRoute, PredictionAccuracy, SystemMetrics
from typing import List, Optional
from datetime import datetime, timedelta

# Route CRUD

def create_route(db: Session, route_data: dict) -> Route:
    """Create a new route"""
    route = Route(**route_data)
    db.add(route)
    db.commit()
    db.refresh(route)
    return route

def get_all_routes(db: Session) -> List[Route]:
    """Get all active routes"""
    return db.execute(select(Route).where(Route.is_active == True)).scalars().all()

def get_route_by_name(db: Session, route_name: str) -> Optional[Route]:
    """Get route by name"""
    return db.execute(select(Route).where(Route.route_name == route_name)).scalar_one_or_none()

# Prediction CRUD

def create_prediction(db: Session, prediction_data: dict) -> Prediction:
    """Save a prediction to database"""
    prediction = Prediction(**prediction_data)
    db.add(prediction)
    db.commit()
    db.refresh(prediction)
    return prediction

def get_recent_predictions(db: Session, route: str = None, limit: int = 100) -> List[Prediction]:
    """Get recent predictions, optionally filtered by route"""
    query = select(Prediction).order_by(desc(Prediction.created_at)).limit(limit)
    
    if route:
        query = query.where(Prediction.route == route)
    
    return db.execute(query).scalars().all()

def get_predictions_by_date_range(
    db: Session, 
    start_date: datetime, 
    end_date: datetime,
    route: str = None
) -> List[Prediction]:
    """Get predictions within a date range"""
    query = select(Prediction).where(
        Prediction.timestamp >= start_date,
        Prediction.timestamp <= end_date
    )
    
    if route:
        query = query.where(Prediction.route == route)
    
    return db.execute(query.order_by(Prediction.timestamp)).scalars().all()

def get_prediction_stats(db: Session, route: str = None) -> dict:
    """Get statistics about predictions"""
    query = select(Prediction)
    
    if route:
        query = query.where(Prediction.route == route)
    
    predictions = db.execute(query).scalars().all()
    
    if not predictions:
        return {"total": 0}
    
    congestion_scores = [p.predicted_congestion for p in predictions]
    
    return {
        "total": len(predictions),
        "avg_congestion": sum(congestion_scores) / len(congestion_scores),
        "max_congestion": max(congestion_scores),
        "min_congestion": min(congestion_scores),
        "high_congestion_count": sum(1 for p in predictions if p.congestion_level == "High"),
        "moderate_congestion_count": sum(1 for p in predictions if p.congestion_level == "Moderate"),
        "low_congestion_count": sum(1 for p in predictions if p.congestion_level == "Low")
    }

# User Routes CRUD

def create_user_route(db: Session, user_route_data: dict) -> UserRoute:
    """Save a user's favorite route"""
    user_route = UserRoute(**user_route_data)
    db.add(user_route)
    db.commit()
    db.refresh(user_route)
    return user_route

def get_user_routes(db: Session, user_id: str) -> List[UserRoute]:
    """Get all routes for a user"""
    return db.execute(
        select(UserRoute).where(UserRoute.user_id == user_id)
    ).scalars().all()

# System Metrics CRUD

def update_system_metrics(db: Session, metrics_data: dict):
    """Update or create system metrics for today"""
    today = datetime.now().date()
    
    # Check if metrics exist for today
    existing = db.execute(
        select(SystemMetrics).where(func.date(SystemMetrics.date) == today)
    ).scalar_one_or_none()
    
    if existing:
        for key, value in metrics_data.items():
            setattr(existing, key, value)
        db.commit()
        return existing
    else:
        metrics = SystemMetrics(**metrics_data, date=datetime.now())
        db.add(metrics)
        db.commit()
        db.refresh(metrics)
        return metrics

def get_system_metrics(db: Session, days: int = 30) -> List[SystemMetrics]:
    """Get system metrics for the last N days"""
    cutoff_date = datetime.now() - timedelta(days=days)
    
    return db.execute(
        select(SystemMetrics).where(SystemMetrics.date >= cutoff_date).order_by(SystemMetrics.date)
    ).scalars().all()

# Statistics

def get_total_predictions(db: Session) -> int:
    """Get total number of predictions made"""
    return db.execute(select(func.count(Prediction.id))).scalar()

def get_most_queried_routes(db: Session, limit: int = 10) -> List[tuple]:
    """Get most frequently queried routes"""
    return db.execute(
        select(Prediction.route, func.count(Prediction.id).label('count'))
        .group_by(Prediction.route)
        .order_by(desc('count'))
        .limit(limit)
    ).all()

def get_hourly_prediction_distribution(db: Session) -> List[tuple]:
    """Get distribution of predictions by hour"""
    return db.execute(
        select(Prediction.hour, func.count(Prediction.id).label('count'))
        .group_by(Prediction.hour)
        .order_by(Prediction.hour)
    ).all()