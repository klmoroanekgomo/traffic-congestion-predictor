# 🚦 Traffic Congestion Prediction System

A machine learning system that predicts traffic congestion levels for major routes in Johannesburg, South Africa. This project demonstrates end-to-end ML pipeline development, from data generation to API deployment.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3+-orange.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 🎯 Project Overview

This system uses machine learning to predict traffic congestion scores (0-100 scale) based on:
- **Time features**: Hour of day, day of week, holidays
- **Route information**: 14 major Johannesburg routes
- **Weather conditions**: Clear, Rain, Cloudy, Drizzle
- **Historical patterns**: Rush hours, weekend effects

### Key Features
- ✅ **99% Prediction Accuracy** (R² = 0.9901)
- ✅ **Real-time API** with FastAPI
- ✅ **Synthetic Data Generation** based on realistic traffic patterns
- ✅ **Multiple ML Models** (XGBoost, Random Forest, Gradient Boosting)
- ✅ **Interactive API Documentation** (Swagger UI)
- ✅ **Comprehensive Visualizations** and EDA

## 📊 Model Performance

| Model | Test R² | Test MAE | Test RMSE |
|-------|---------|----------|-----------|
| **XGBoost** ⭐ | **0.9902** | **1.847** | **2.397** |
| Gradient Boosting | 0.9900 | 1.872 | 2.418 |
| Random Forest | 0.9894 | 1.915 | 2.494 |
| Linear Regression | 0.9893 | 1.975 | 2.500 |

**Best Model**: XGBoost with 99.01% accuracy

## 🛠️ Tech Stack

- **Language**: Python 3.10+
- **ML Libraries**: scikit-learn, XGBoost
- **API Framework**: FastAPI, Uvicorn
- **Data Processing**: pandas, numpy
- **Visualization**: matplotlib, seaborn
- **Model Persistence**: joblib

## 📁 Project Structure
```
traffic-congestion-predictor/
├── data/
│   ├── raw/                    # Raw traffic data
│   └── processed/              # Processed features
├── notebooks/
│   └── 01_exploratory_data_analysis.ipynb
├── src/
│   ├── data_processing/
│   │   ├── generate_synthetic_data.py
│   │   └── feature_engineering.py
│   ├── models/
│   │   └── train_model.py
│   └── api/
│       ├── main.py            # FastAPI application
│       └── test_api.py        # API tests
├── models/                     # Trained models
│   ├── best_model.pkl
│   ├── model_info.pkl
│   └── label_encoders.pkl
├── tests/                      # Unit tests
├── requirements.txt
└── README.md
```

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- pip package manager
- Virtual environment (recommended)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/traffic-congestion-predictor.git
cd traffic-congestion-predictor
```

2. **Create and activate virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

### Generate Data
```bash
python src/data_processing/generate_synthetic_data.py
```

This creates ~500,000 records of realistic traffic data for 14 Johannesburg routes.

### Train Models
```bash
# Feature engineering
python src/data_processing/feature_engineering.py

# Train and evaluate models
python src/models/train_model.py
```

### Run the API
```bash
python src/api/main.py
```

The API will be available at `http://localhost:8000`

## 📖 API Usage

### Interactive Documentation

Visit `http://localhost:8000/docs` for interactive Swagger UI documentation.

### Example Request (Python)
```python
import requests

# Single prediction
response = requests.post(
    "http://localhost:8000/predict",
    json={
        "timestamp": "2024-06-15 08:30:00",
        "route": "M1_North",
        "weather": "Clear",
        "temperature": 18.5,
        "is_holiday": False
    }
)

result = response.json()
print(f"Congestion Score: {result['congestion_score']}")
print(f"Congestion Level: {result['congestion_level']}")
```

### Example Request (cURL)
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "timestamp": "2024-06-15 17:30:00",
    "route": "N1_South",
    "weather": "Rain",
    "temperature": 15.0,
    "is_holiday": false
  }'
```

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information |
| `/health` | GET | Health check |
| `/predict` | POST | Single prediction |
| `/batch-predict` | POST | Batch predictions |
| `/model/info` | GET | Model metadata |
| `/routes` | GET | Available routes |
| `/weather-conditions` | GET | Valid weather conditions |

## 📈 Key Insights from EDA

- **Peak congestion hours**: 6-9 AM and 4-7 PM (rush hours)
- **Weather impact**: Rain increases congestion by ~15-20 points
- **Weekend effect**: 20-25% lower congestion on weekends
- **Most congested routes**: M1 and N1 highways
- **Holiday effect**: Significant reduction in traffic

## 🧪 Testing

Run API tests:
```bash
python src/api/test_api.py
```

## 🔮 Future Enhancements

- [ ] Integration with real-time traffic APIs (Google Maps, TomTom)
- [ ] LSTM model for time-series predictions
- [ ] Mobile application interface
- [ ] Real-time traffic alerts
- [ ] Route optimization recommendations
- [ ] Docker containerization
- [ ] CI/CD pipeline with GitHub Actions

## 📊 Visualizations

The project includes comprehensive visualizations:
- Hourly congestion patterns
- Day-of-week analysis
- Weather impact analysis
- Route comparisons
- Feature importance plots
- Model performance comparisons

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**[Your Name]**
- BSc Computer Science Graduate
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/yourprofile)

## 🙏 Acknowledgments

- Traffic patterns based on Johannesburg metropolitan area
- Synthetic data generation inspired by real-world traffic behavior
- FastAPI for the excellent web framework
- scikit-learn and XGBoost communities

## 📧 Contact

For questions or feedback, please open an issue or contact me at your.email@example.com

---

⭐ If you found this project helpful, please consider giving it a star!