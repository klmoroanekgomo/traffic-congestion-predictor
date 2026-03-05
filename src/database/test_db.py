"""
Test traffic database
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.database.database import SessionLocal
from src.database import crud
from datetime import datetime

def test_database():
    print("="*70)
    print("TESTING TRAFFIC DATABASE")
    print("="*70)
    
    db = SessionLocal()
    
    try:
        # Test 1: Get routes
        print("\n1️⃣  Getting all routes...")
        routes = crud.get_all_routes(db)
        print(f"✓ Found {len(routes)} routes")
        for route in routes[:3]:
            print(f"  • {route.route_name}")
        
        # Test 2: Create prediction
        print("\n2️⃣  Creating test prediction...")
        prediction_data = {
            "route": "M1_North",
            "timestamp": datetime.now(),
            "hour": 8,
            "day_of_week": 1,
            "is_weekend": False,
            "is_holiday": False,
            "month": 3,
            "weather": "Clear",
            "temperature": 22.5,
            "predicted_congestion": 65.5,
            "congestion_level": "High",
            "model_used": "XGBoost"
        }
        
        prediction = crud.create_prediction(db, prediction_data)
        print(f"✓ Prediction created: {prediction.id}")
        
        # Test 3: Get statistics
        print("\n3️⃣  Getting prediction statistics...")
        total = crud.get_total_predictions(db)
        print(f"✓ Total predictions: {total}")
        
        stats = crud.get_prediction_stats(db, "M1_North")
        print(f"✓ M1_North stats: {stats}")
        
        print("\n" + "="*70)
        print("✅ ALL TESTS PASSED!")
        print("="*70)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_database()