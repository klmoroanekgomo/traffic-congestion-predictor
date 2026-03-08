"""
Weather service for fetching real-time weather data
"""

import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

class WeatherService:
    """Fetch weather data from OpenWeatherMap API"""
    
    def __init__(self):
        self.api_key = os.getenv('OPENWEATHER_API_KEY')
        self.lat = float(os.getenv('JOHANNESBURG_LAT', -26.2041))
        self.lon = float(os.getenv('JOHANNESBURG_LON', 28.0473))
        self.base_url = "https://api.openweathermap.org/data/2.5"
    
    def get_current_weather(self):
        """
        Get current weather for Johannesburg
        
        Returns:
        --------
        dict
            Weather information including temperature, conditions, etc.
        """
        
        if not self.api_key:
            return self._get_mock_weather()
        
        try:
            url = f"{self.base_url}/weather"
            params = {
                'lat': self.lat,
                'lon': self.lon,
                'appid': self.api_key,
                'units': 'metric'  # Celsius
            }
            
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            
            return {
                'temperature': data['main']['temp'],
                'feels_like': data['main']['feels_like'],
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'weather': data['weather'][0]['main'],
                'description': data['weather'][0]['description'],
                'wind_speed': data['wind']['speed'],
                'clouds': data['clouds']['all'],
                'timestamp': datetime.fromtimestamp(data['dt'])
            }
            
        except Exception as e:
            print(f"Error fetching weather: {e}")
            return self._get_mock_weather()
    
    def get_weather_forecast(self, hours=24):
        """
        Get weather forecast for next N hours
        
        Parameters:
        -----------
        hours : int
            Number of hours to forecast (max 120)
            
        Returns:
        --------
        list
            List of weather forecasts
        """
        
        if not self.api_key:
            return [self._get_mock_weather() for _ in range(hours // 3)]
        
        try:
            url = f"{self.base_url}/forecast"
            params = {
                'lat': self.lat,
                'lon': self.lon,
                'appid': self.api_key,
                'units': 'metric',
                'cnt': min(hours // 3, 40)  # API returns 3-hour intervals
            }
            
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            
            forecasts = []
            for item in data['list']:
                forecasts.append({
                    'timestamp': datetime.fromtimestamp(item['dt']),
                    'temperature': item['main']['temp'],
                    'feels_like': item['main']['feels_like'],
                    'humidity': item['main']['humidity'],
                    'weather': item['weather'][0]['main'],
                    'description': item['weather'][0]['description'],
                    'wind_speed': item['wind']['speed'],
                    'clouds': item['clouds']['all'],
                    'rain_probability': item.get('pop', 0) * 100  # Probability of precipitation
                })
            
            return forecasts
            
        except Exception as e:
            print(f"Error fetching forecast: {e}")
            return [self._get_mock_weather() for _ in range(hours // 3)]
    
    def _get_mock_weather(self):
        """Return mock weather data when API is unavailable"""
        return {
            'temperature': 20.0,
            'feels_like': 20.0,
            'humidity': 60,
            'pressure': 1013,
            'weather': 'Clear',
            'description': 'clear sky',
            'wind_speed': 3.5,
            'clouds': 0,
            'timestamp': datetime.now()
        }
    
    def map_to_model_format(self, weather_data):
        """
        Convert weather API data to model input format
        
        Parameters:
        -----------
        weather_data : dict
            Weather data from API
            
        Returns:
        --------
        dict
            Weather data in model format
        """
        
        # Map API weather types to our model's categories
        weather_mapping = {
            'Clear': 'Clear',
            'Clouds': 'Cloudy',
            'Rain': 'Rain',
            'Drizzle': 'Drizzle',
            'Thunderstorm': 'Rain',
            'Snow': 'Cloudy',
            'Mist': 'Cloudy',
            'Fog': 'Cloudy'
        }
        
        weather_condition = weather_mapping.get(
            weather_data['weather'],
            'Clear'
        )
        
        return {
            'weather': weather_condition,
            'temperature': weather_data['temperature']
        }


def main():
    """Test weather service"""
    
    print("="*70)
    print("WEATHER SERVICE TEST")
    print("="*70)
    
    service = WeatherService()
    
    # Test current weather
    print("\n🌤️  CURRENT WEATHER")
    print("-"*70)
    current = service.get_current_weather()
    
    print(f"Temperature: {current['temperature']:.1f}°C")
    print(f"Feels Like: {current['feels_like']:.1f}°C")
    print(f"Condition: {current['weather']} - {current['description']}")
    print(f"Humidity: {current['humidity']}%")
    print(f"Wind Speed: {current['wind_speed']} m/s")
    print(f"Time: {current['timestamp']}")
    
    # Test forecast
    print("\n📅 24-HOUR FORECAST")
    print("-"*70)
    forecast = service.get_weather_forecast(24)
    
    for i, f in enumerate(forecast[:8], 1):
        print(f"{i}. {f['timestamp'].strftime('%H:%M')} - "
              f"{f['temperature']:.1f}°C - {f['weather']} "
              f"({f['rain_probability']:.0f}% rain)")
    
    # Test model format conversion
    print("\n🔄 MODEL FORMAT")
    print("-"*70)
    model_format = service.map_to_model_format(current)
    print(f"Weather: {model_format['weather']}")
    print(f"Temperature: {model_format['temperature']:.1f}°C")
    
    print("\n" + "="*70)
    print("✅ WEATHER SERVICE TEST COMPLETE")
    print("="*70)

if __name__ == "__main__":
    main()