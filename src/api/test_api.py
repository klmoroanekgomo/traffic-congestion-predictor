"""
Test script for the Traffic Congestion Prediction API
"""

import requests
import json
from datetime import datetime, timedelta

# API base URL
BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test the health check endpoint"""
    print("\n" + "="*60)
    print("Testing Health Check Endpoint")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
def test_model_info():
    """Test the model info endpoint"""
    print("\n" + "="*60)
    print("Testing Model Info Endpoint")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/model/info")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_single_prediction():
    """Test single prediction endpoint"""
    print("\n" + "="*60)
    print("Testing Single Prediction - Morning Rush Hour")
    print("="*60)
    
    # Morning rush hour on a weekday
    payload = {
        "timestamp": "2024-06-15 08:30:00",
        "route": "M1_North",
        "weather": "Clear",
        "temperature": 18.5,
        "is_holiday": False
    }
    
    response = requests.post(f"{BASE_URL}/predict", json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Request: {json.dumps(payload, indent=2)}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
def test_rainy_rush_hour():
    """Test prediction during rainy rush hour"""
    print("\n" + "="*60)
    print("Testing Prediction - Rainy Evening Rush Hour")
    print("="*60)
    
    payload = {
        "timestamp": "2024-06-15 17:30:00",
        "route": "N1_South",
        "weather": "Rain",
        "temperature": 15.0,
        "is_holiday": False
    }
    
    response = requests.post(f"{BASE_URL}/predict", json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Request: {json.dumps(payload, indent=2)}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_weekend_prediction():
    """Test prediction for weekend"""
    print("\n" + "="*60)
    print("Testing Prediction - Weekend Afternoon")
    print("="*60)
    
    payload = {
        "timestamp": "2024-06-15 14:00:00",  # Saturday
        "route": "Sandton_Drive",
        "weather": "Cloudy",
        "temperature": 20.0,
        "is_holiday": False
    }
    
    response = requests.post(f"{BASE_URL}/predict", json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Request: {json.dumps(payload, indent=2)}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_batch_prediction():
    """Test batch prediction endpoint"""
    print("\n" + "="*60)
    print("Testing Batch Prediction - Multiple Routes")
    print("="*60)
    
    payload = {
        "predictions": [
            {
                "timestamp": "2024-06-15 08:00:00",
                "route": "M1_North",
                "weather": "Clear",
                "temperature": 18.0,
                "is_holiday": False
            },
            {
                "timestamp": "2024-06-15 08:00:00",
                "route": "N1_South",
                "weather": "Clear",
                "temperature": 18.0,
                "is_holiday": False
            },
            {
                "timestamp": "2024-06-15 08:00:00",
                "route": "M2_East",
                "weather": "Clear",
                "temperature": 18.0,
                "is_holiday": False
            }
        ]
    }
    
    response = requests.post(f"{BASE_URL}/batch-predict", json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_routes_endpoint():
    """Test available routes endpoint"""
    print("\n" + "="*60)
    print("Testing Available Routes Endpoint")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/routes")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def main():
    """Run all tests"""
    print("="*60)
    print("TRAFFIC CONGESTION PREDICTION API - TEST SUITE")
    print("="*60)
    print(f"Testing API at: {BASE_URL}")
    print("Make sure the API is running before executing tests!")
    print("="*60)
    
    try:
        # Run all tests
        test_health_check()
        test_model_info()
        test_routes_endpoint()
        test_single_prediction()
        test_rainy_rush_hour()
        test_weekend_prediction()
        test_batch_prediction()
        
        print("\n" + "="*60)
        print("✓ ALL TESTS COMPLETED SUCCESSFULLY")
        print("="*60)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to API")
        print("Make sure the API is running: python src/api/main.py")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")

if __name__ == "__main__":
    main()