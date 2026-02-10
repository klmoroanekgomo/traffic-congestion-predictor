"""
Feature Engineering for Traffic Congestion Prediction
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import joblib
import os

class FeatureEngineer:
    """Create and transform features for ML models"""
    
    def __init__(self):
        self.label_encoders = {}
        
    def create_features(self, df):
        """
        Create additional features from the dataset
        
        Parameters:
        -----------
        df : pd.DataFrame
            Input dataframe
            
        Returns:
        --------
        pd.DataFrame
            Dataframe with engineered features
        """
        
        df = df.copy()
        
        # Ensure timestamp is datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        print("Creating time-based features...")
        
        # Time-based features
        df['year'] = df['timestamp'].dt.year
        df['month'] = df['timestamp'].dt.month
        df['day'] = df['timestamp'].dt.day
        df['hour'] = df['timestamp'].dt.hour
        df['minute'] = df['timestamp'].dt.minute
        df['day_of_week'] = df['timestamp'].dt.dayofweek
        df['day_of_year'] = df['timestamp'].dt.dayofyear
        df['week_of_year'] = df['timestamp'].dt.isocalendar().week
        df['quarter'] = df['timestamp'].dt.quarter
        
        # Cyclical features (important for time patterns)
        df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 24)
        df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 24)
        df['day_sin'] = np.sin(2 * np.pi * df['day_of_week'] / 7)
        df['day_cos'] = np.cos(2 * np.pi * df['day_of_week'] / 7)
        df['month_sin'] = np.sin(2 * np.pi * df['month'] / 12)
        df['month_cos'] = np.cos(2 * np.pi * df['month'] / 12)
        
        print("Creating categorical features...")
        
        # Rush hour indicators
        df['is_morning_rush'] = ((df['hour'] >= 6) & (df['hour'] <= 9)).astype(int)
        df['is_evening_rush'] = ((df['hour'] >= 16) & (df['hour'] <= 19)).astype(int)
        df['is_rush_hour'] = (df['is_morning_rush'] | df['is_evening_rush']).astype(int)
        
        # Time of day categories
        df['time_of_day'] = pd.cut(df['hour'], 
                                   bins=[0, 6, 12, 18, 24], 
                                   labels=['Night', 'Morning', 'Afternoon', 'Evening'],
                                   include_lowest=True)
        
        # Working hours
        df['is_working_hours'] = ((df['hour'] >= 8) & (df['hour'] <= 17) & 
                                  (~df['is_weekend'])).astype(int)
        
        print("Creating interaction features...")
        
        # Interaction features
        df['weekend_rush'] = df['is_weekend'] * df['is_rush_hour']
        df['holiday_weekend'] = df['is_holiday'] * df['is_weekend']
        df['rain_rush'] = (df['weather'] == 'Rain').astype(int) * df['is_rush_hour']
        
        # Route type (highway vs regular road)
        df['is_highway'] = df['route'].str.contains('N1|N3|M1|M2').astype(int)
        
        print(f"✓ Created {len(df.columns)} total features")
        
        return df
    
    def encode_categorical(self, df, categorical_cols, fit=True):
        """
        Encode categorical variables
        
        Parameters:
        -----------
        df : pd.DataFrame
            Input dataframe
        categorical_cols : list
            List of categorical column names
        fit : bool
            Whether to fit the encoders (True for training, False for test)
            
        Returns:
        --------
        pd.DataFrame
            Dataframe with encoded categorical variables
        """
        
        df = df.copy()
        
        for col in categorical_cols:
            if col in df.columns:
                if fit:
                    le = LabelEncoder()
                    df[f'{col}_encoded'] = le.fit_transform(df[col].astype(str))
                    self.label_encoders[col] = le
                else:
                    if col in self.label_encoders:
                        le = self.label_encoders[col]
                        df[f'{col}_encoded'] = le.transform(df[col].astype(str))
                    else:
                        raise ValueError(f"No encoder found for {col}")
        
        return df
    
    def prepare_data_for_ml(self, df, target_col='congestion_score', 
                           categorical_cols=None):
        """
        Prepare data for machine learning
        
        Parameters:
        -----------
        df : pd.DataFrame
            Input dataframe
        target_col : str
            Name of target variable
        categorical_cols : list
            List of categorical columns to encode
            
        Returns:
        --------
        tuple
            (features_df, target_series, feature_names)
        """
        
        if categorical_cols is None:
            categorical_cols = ['route', 'weather', 'day_name', 'time_of_day']
        
        # Create features
        df = self.create_features(df)
        
        # Encode categorical variables
        df = self.encode_categorical(df, categorical_cols, fit=True)
        
        # Define feature columns (exclude non-feature columns)
        exclude_cols = ['timestamp', 'congestion_level', target_col, 
                       'route', 'weather', 'day_name', 'time_of_day']
        
        feature_cols = [col for col in df.columns if col not in exclude_cols]
        
        X = df[feature_cols]
        y = df[target_col]
        
        print(f"\n{'='*60}")
        print("DATA PREPARATION SUMMARY")
        print("="*60)
        print(f"Total samples: {len(X):,}")
        print(f"Number of features: {len(feature_cols)}")
        print(f"Target variable: {target_col}")
        print(f"Target range: [{y.min():.2f}, {y.max():.2f}]")
        print(f"Target mean: {y.mean():.2f}")
        print("="*60)
        
        return X, y, feature_cols
    
    def save_encoders(self, filepath='models/label_encoders.pkl'):
        """Save label encoders"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        joblib.dump(self.label_encoders, filepath)
        print(f"✓ Encoders saved to {filepath}")
    
    def load_encoders(self, filepath='models/label_encoders.pkl'):
        """Load label encoders"""
        self.label_encoders = joblib.load(filepath)
        print(f"✓ Encoders loaded from {filepath}")


def main():
    """Main function to demonstrate feature engineering"""
    
    print("="*60)
    print("FEATURE ENGINEERING PIPELINE")
    print("="*60)
    
    # Load data
    print("\nLoading data...")
    df = pd.read_csv('data/raw/traffic_data.csv')
    print(f"✓ Loaded {len(df):,} records")
    
    # Initialize feature engineer
    fe = FeatureEngineer()
    
    # Prepare data
    X, y, feature_names = fe.prepare_data_for_ml(df)
    
    print(f"\nFeature names:")
    for i, name in enumerate(feature_names, 1):
        print(f"{i:2d}. {name}")
    
    # Save processed data
    print("\nSaving processed data...")
    X.to_csv('data/processed/X_features.csv', index=False)
    y.to_csv('data/processed/y_target.csv', index=False, header=True)
    
    # Save feature names
    pd.DataFrame({'feature': feature_names}).to_csv(
        'data/processed/feature_names.csv', index=False
    )
    
    # Save encoders
    fe.save_encoders()
    
    print("\n" + "="*60)
    print("FEATURE ENGINEERING COMPLETE!")
    print("="*60)
    print("\nProcessed files saved:")
    print("  • data/processed/X_features.csv")
    print("  • data/processed/y_target.csv")
    print("  • data/processed/feature_names.csv")
    print("  • models/label_encoders.pkl")
    print("="*60)
    
    return X, y, feature_names


if __name__ == "__main__":
    X, y, feature_names = main()