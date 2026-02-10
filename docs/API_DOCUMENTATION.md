# API Documentation

## Base URL
```
http://localhost:8000
```

## Endpoints

### 1. Root Endpoint
**GET** `/`

Returns API information and available endpoints.

**Response:**
```json
{
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
```

### 2. Health Check
**GET** `/health`

Check if the API and model are loaded successfully.

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "timestamp": "2024-02-10T14:30:00"
}
```

### 3. Predict Congestion
**POST** `/predict`

Predict traffic congestion for a specific time, route, and conditions.

**Request Body:**
```json
{
  "timestamp": "2024-06-15 08:30:00",
  "route": "M1_North",
  "weather": "Clear",
  "temperature": 18.5,
  "is_holiday": false
}
```

**Parameters:**
- `timestamp` (string, required): Date and time in format "YYYY-MM-DD HH:MM:SS"
- `route` (string, required): Route name from available routes
- `weather` (string, required): Weather condition (Clear, Rain, Cloudy, Drizzle)
- `temperature` (float, required): Temperature in Celsius
- `is_holiday` (boolean, optional): Whether it's a public holiday (default: false)

**Response:**
```json
{
  "congestion_score": 62.45,
  "congestion_level": "High",
  "timestamp": "2024-06-15 08:30:00",
  "route": "M1_North",
  "weather": "Clear",
  "model_used": "XGBoost",
  "confidence": "High"
}
```

### 4. Batch Prediction
**POST** `/batch-predict`

Predict congestion for multiple requests at once.

**Request Body:**
```json
{
  "predictions": [
    {
      "timestamp": "2024-06-15 08:00:00",
      "route": "M1_North",
      "weather": "Clear",
      "temperature": 18.0,
      "is_holiday": false
    },
    {
      "timestamp": "2024-06-15 08:00:00",
      "route": "N1_South",
      "weather": "Rain",
      "temperature": 16.0,
      "is_holiday": false
    }
  ]
}
```

**Response:**
```json
{
  "predictions": [
    {
      "congestion_score": 62.45,
      "congestion_level": "High",
      ...
    },
    {
      "congestion_score": 75.30,
      "congestion_level": "High",
      ...
    }
  ],
  "count": 2,
  "model_used": "XGBoost"
}
```

### 5. Model Information
**GET** `/model/info`

Get information about the trained model.

**Response:**
```json
{
  "model_name": "XGBoost",
  "training_date": "2024-02-10 14:00:00",
  "n_features": 32,
  "n_samples": 490574,
  "metrics": {
    "val_r2": 0.9901,
    "val_mae": 1.858,
    "test_r2": 0.9902,
    "test_mae": 1.847
  }
}
```

### 6. Available Routes
**GET** `/routes`

Get list of all available routes.

**Response:**
```json
{
  "routes": [
    "M1_North",
    "M1_South",
    "N1_North",
    "N1_South",
    "N3_East",
    "N3_West",
    "M2_East",
    "M2_West",
    "William_Nicol",
    "Rivonia_Road",
    "Jan_Smuts",
    "Sandton_Drive",
    "Pretoria_Main",
    "Soweto_Highway"
  ],
  "count": 14
}
```

### 7. Weather Conditions
**GET** `/weather-conditions`

Get list of valid weather conditions.

**Response:**
```json
{
  "weather_conditions": [
    "Clear",
    "Rain",
    "Cloudy",
    "Drizzle"
  ],
  "count": 4
}
```

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Prediction error: Invalid timestamp format"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Model not loaded"
}
```

## Congestion Levels

| Score Range | Level | Description |
|-------------|-------|-------------|
| 0-30 | Low | Free-flowing traffic |
| 30-60 | Moderate | Some delays expected |
| 60-100 | High | Significant congestion |
```

### Step 4: Create a LICENSE File

Create `LICENSE` file:
```
MIT License

Copyright (c) 2024 [Kgaiso Moroane-Kgomo]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.