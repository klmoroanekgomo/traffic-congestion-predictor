"""
Generate synthetic traffic data for Johannesburg routes
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

class TrafficDataGenerator:
    """Generate realistic synthetic traffic data"""
    
    def __init__(self, seed=42):
        """Initialize the generator with a random seed for reproducibility"""
        np.random.seed(seed)
        random.seed(seed)
        
        # Define major Johannesburg routes
        self.routes = [
            'M1_North', 'M1_South', 'N1_North', 'N1_South',
            'N3_East', 'N3_West', 'M2_East', 'M2_West',
            'William_Nicol', 'Rivonia_Road', 'Jan_Smuts',
            'Sandton_Drive', 'Pretoria_Main', 'Soweto_Highway'
        ]
        
        # Weather conditions
        self.weather_conditions = ['Clear', 'Rain', 'Cloudy', 'Drizzle']
        
        # South African public holidays (2024)
        self.public_holidays = [
            '2024-01-01', '2024-03-21', '2024-03-29', '2024-04-01',
            '2024-04-27', '2024-05-01', '2024-06-16', '2024-08-09',
            '2024-09-24', '2024-12-16', '2024-12-25', '2024-12-26'
        ]
    
    def generate_data(self, start_date='2024-01-01', end_date='2024-12-31', 
                     interval_minutes=15):
        """
        Generate synthetic traffic data
        
        Parameters:
        -----------
        start_date : str
            Start date for data generation
        end_date : str
            End date for data generation
        interval_minutes : int
            Time interval between records (in minutes)
        
        Returns:
        --------
        pd.DataFrame
            Generated traffic data
        """
        
        # Generate datetime range
        start = pd.to_datetime(start_date)
        end = pd.to_datetime(end_date)
        date_range = pd.date_range(start=start, end=end, 
                                   freq=f'{interval_minutes}min')
        
        data = []
        
        print("Generating traffic records...")
        total_timestamps = len(date_range)
        
        for idx, timestamp in enumerate(date_range):
            if idx % 1000 == 0:
                print(f"Progress: {idx}/{total_timestamps} timestamps processed...")
            
            for route in self.routes:
                record = self._generate_record(timestamp, route)
                data.append(record)
        
        print("Creating DataFrame...")
        df = pd.DataFrame(data)
        return df
    
    def _generate_record(self, timestamp, route):
        """Generate a single traffic record"""
        
        # Extract time features
        hour = timestamp.hour
        day_of_week = timestamp.dayofweek  # 0=Monday, 6=Sunday
        is_weekend = day_of_week >= 5
        is_holiday = timestamp.strftime('%Y-%m-%d') in self.public_holidays
        month = timestamp.month
        
        # Base congestion level (0-100 scale)
        congestion = 20  # Base level
        
        # Time of day patterns
        # Morning rush hour (6-9 AM)
        if 6 <= hour <= 9:
            congestion += 40 + np.random.normal(0, 5)
        # Evening rush hour (4-7 PM)
        elif 16 <= hour <= 19:
            congestion += 45 + np.random.normal(0, 5)
        # Lunch time (12-2 PM)
        elif 12 <= hour <= 14:
            congestion += 15 + np.random.normal(0, 3)
        # Late night (11 PM - 5 AM)
        elif hour >= 23 or hour <= 5:
            congestion -= 10 + np.random.normal(0, 2)
        
        # Weekend patterns (less congestion)
        if is_weekend:
            congestion -= 20
            # But shopping areas busy on Saturday afternoon
            if day_of_week == 5 and 10 <= hour <= 15:
                congestion += 10
        
        # Holiday patterns (reduced traffic)
        if is_holiday:
            congestion -= 25
        
        # Weather impact
        weather = np.random.choice(
            self.weather_conditions,
            p=[0.6, 0.15, 0.20, 0.05]  # Probabilities
        )
        
        if weather == 'Rain':
            congestion += 15 + np.random.normal(0, 3)
        elif weather == 'Drizzle':
            congestion += 8 + np.random.normal(0, 2)
        
        # Route-specific adjustments
        if 'M1' in route or 'N1' in route:  # Major highways
            congestion += 5
        
        # Add some random variation
        congestion += np.random.normal(0, 5)
        
        # Ensure congestion is within bounds
        congestion = max(0, min(100, congestion))
        
        # Calculate average speed (inverse relationship with congestion)
        # Assume max speed is 120 km/h, min is 20 km/h
        avg_speed = 120 - (congestion * 0.8) + np.random.normal(0, 3)
        avg_speed = max(20, min(120, avg_speed))
        
        # Traffic volume (vehicles per hour)
        traffic_volume = int(congestion * 50 + np.random.normal(0, 200))
        traffic_volume = max(0, traffic_volume)
        
        # Congestion level classification
        if congestion < 30:
            congestion_level = 'Low'
        elif congestion < 60:
            congestion_level = 'Moderate'
        else:
            congestion_level = 'High'
        
        return {
            'timestamp': timestamp,
            'route': route,
            'hour': hour,
            'day_of_week': day_of_week,
            'day_name': timestamp.strftime('%A'),
            'is_weekend': is_weekend,
            'is_holiday': is_holiday,
            'month': month,
            'weather': weather,
            'temperature': np.random.normal(20, 5),  # Average temp in JHB
            'congestion_score': round(congestion, 2),
            'congestion_level': congestion_level,
            'avg_speed_kmh': round(avg_speed, 2),
            'traffic_volume': traffic_volume
        }

def main():
    """Main function to generate and save traffic data"""
    
    print("=" * 60)
    print("TRAFFIC DATA GENERATOR - JOHANNESBURG")
    print("=" * 60)
    print("\nGenerating synthetic traffic data...")
    
    generator = TrafficDataGenerator(seed=42)
    
    # Generate one year of data with 15-minute intervals
    df = generator.generate_data(
        start_date='2024-01-01',
        end_date='2024-12-31',
        interval_minutes=15
    )
    
    print("\n" + "=" * 60)
    print("GENERATION COMPLETE!")
    print("=" * 60)
    print(f"\nTotal records generated: {len(df):,}")
    print(f"Data shape: {df.shape}")
    print(f"Routes covered: {df['route'].nunique()}")
    print(f"Date range: {df['timestamp'].min()} to {df['timestamp'].max()}")
    
    print(f"\n{'='*60}")
    print("SAMPLE DATA (First 5 records):")
    print("=" * 60)
    print(df.head())
    
    print(f"\n{'='*60}")
    print("CONGESTION LEVEL DISTRIBUTION:")
    print("=" * 60)
    print(df['congestion_level'].value_counts())
    
    print(f"\n{'='*60}")
    print("WEATHER DISTRIBUTION:")
    print("=" * 60)
    print(df['weather'].value_counts())
    
    # Save to CSV
    output_path = 'data/raw/traffic_data.csv'
    print(f"\n{'='*60}")
    print(f"Saving data to: {output_path}")
    print("=" * 60)
    df.to_csv(output_path, index=False)
    print("✓ Data saved successfully!")
    
    print(f"\n{'='*60}")
    print("NEXT STEPS:")
    print("=" * 60)
    print("1. Check the data file in: data/raw/traffic_data.csv")
    print("2. Review the data statistics above")
    print("3. Ready to move to Exploratory Data Analysis (EDA)")
    print("=" * 60)
    
    return df

if __name__ == "__main__":
    df = main()