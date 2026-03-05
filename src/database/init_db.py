"""
Initialize Traffic Congestion database
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.database.database import engine, SessionLocal
from src.database.models import Base, Route
from src.database import crud

# Johannesburg routes
ROUTES = [
    {"route_name": "M1_North", "description": "M1 Highway heading North"},
    {"route_name": "M1_South", "description": "M1 Highway heading South"},
    {"route_name": "N1_North", "description": "N1 Highway heading North"},
    {"route_name": "N1_South", "description": "N1 Highway heading South"},
    {"route_name": "N3_East", "description": "N3 Highway heading East"},
    {"route_name": "N3_West", "description": "N3 Highway heading West"},
    {"route_name": "M2_East", "description": "M2 Highway heading East"},
    {"route_name": "M2_West", "description": "M2 Highway heading West"},
    {"route_name": "William_Nicol", "description": "William Nicol Drive"},
    {"route_name": "Rivonia_Road", "description": "Rivonia Road"},
    {"route_name": "Jan_Smuts", "description": "Jan Smuts Avenue"},
    {"route_name": "Sandton_Drive", "description": "Sandton Drive"},
    {"route_name": "Pretoria_Main", "description": "Pretoria Main Road"},
    {"route_name": "Soweto_Highway", "description": "Soweto Highway"},
]

def init_database():
    """Initialize database tables and seed data"""
    print("="*70)
    print("INITIALIZING TRAFFIC CONGESTION DATABASE")
    print("="*70)
    
    print("\nDropping existing tables...")
    Base.metadata.drop_all(bind=engine)
    
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    
    print("✓ Tables created:")
    print("  • routes")
    print("  • predictions")
    print("  • user_routes")
    print("  • prediction_accuracy")
    print("  • system_metrics")
    
    # Seed routes
    print("\n📍 Seeding routes...")
    db = SessionLocal()
    
    try:
        for route_data in ROUTES:
            route = crud.create_route(db, route_data)
            print(f"  ✓ {route.route_name}")
        
        print(f"\n✓ Seeded {len(ROUTES)} routes")
    except Exception as e:
        print(f"❌ Error seeding routes: {e}")
        db.rollback()
    finally:
        db.close()
    
    print("\n" + "="*70)
    print("DATABASE READY!")
    print("="*70)

if __name__ == "__main__":
    init_database()