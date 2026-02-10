"""
Test script to manually save the trained model
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import xgboost as xgb
import joblib
from datetime import datetime
import os

print("Loading data...")
X = pd.read_csv('data/processed/X_features.csv')
y = pd.read_csv('data/processed/y_target.csv').values.ravel()

print("Splitting data...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("Training XGBoost model...")
model = xgb.XGBRegressor(
    n_estimators=100,
    max_depth=7,
    learning_rate=0.1,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)
print("✓ Model trained")

# Test prediction
from sklearn.metrics import r2_score, mean_absolute_error
y_pred = model.predict(X_test)
r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)

print(f"\nModel Performance:")
print(f"  R² Score: {r2:.4f}")
print(f"  MAE: {mae:.3f}")

# Create models directory if it doesn't exist
os.makedirs('models', exist_ok=True)

# Save model
model_path = 'models/best_model.pkl'
print(f"\nSaving model to {model_path}...")
joblib.dump(model, model_path)
print("✓ Model saved")

# Save model info
model_info = {
    'model_name': 'XGBoost',
    'metrics': {
        'test_r2': r2,
        'test_mae': mae,
        'val_r2': r2,  # Using test as proxy
        'val_mae': mae
    },
    'training_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'n_features': X.shape[1],
    'n_samples': len(X)
}

info_path = 'models/model_info.pkl'
print(f"Saving model info to {info_path}...")
joblib.dump(model_info, info_path)
print("✓ Model info saved")

# Verify files exist
print("\nVerifying files...")
if os.path.exists(model_path):
    size = os.path.getsize(model_path)
    print(f"✓ best_model.pkl exists ({size:,} bytes)")
else:
    print("❌ best_model.pkl NOT FOUND")

if os.path.exists(info_path):
    size = os.path.getsize(info_path)
    print(f"✓ model_info.pkl exists ({size:,} bytes)")
else:
    print("❌ model_info.pkl NOT FOUND")

if os.path.exists('models/label_encoders.pkl'):
    size = os.path.getsize('models/label_encoders.pkl')
    print(f"✓ label_encoders.pkl exists ({size:,} bytes)")
else:
    print("❌ label_encoders.pkl NOT FOUND")

print("\n" + "="*60)
print("DONE! All model files should now be saved.")
print("="*60)