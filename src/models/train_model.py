"""
Train and evaluate machine learning models for traffic prediction
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import xgboost as xgb
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os

class TrafficPredictor:
    """Train and evaluate traffic congestion prediction models"""
    
    def __init__(self, random_state=42):
        self.random_state = random_state
        self.models = {}
        self.results = {}
        self.best_model = None
        self.best_model_name = None
        
    def load_data(self, X_path='data/processed/X_features.csv',
                  y_path='data/processed/y_target.csv'):
        """Load processed data"""
        print("Loading processed data...")
        self.X = pd.read_csv(X_path)
        self.y = pd.read_csv(y_path).values.ravel()
        print(f"✓ Loaded {len(self.X):,} samples with {self.X.shape[1]} features")
        
    def split_data(self, test_size=0.2, val_size=0.1):
        """Split data into train, validation, and test sets"""
        print("\nSplitting data...")
        
        # First split: separate test set
        X_temp, self.X_test, y_temp, self.y_test = train_test_split(
            self.X, self.y, test_size=test_size, random_state=self.random_state
        )
        
        # Second split: separate validation set from training
        val_ratio = val_size / (1 - test_size)
        self.X_train, self.X_val, self.y_train, self.y_val = train_test_split(
            X_temp, y_temp, test_size=val_ratio, random_state=self.random_state
        )
        
        print(f"  Training set:   {len(self.X_train):,} samples ({len(self.X_train)/len(self.X)*100:.1f}%)")
        print(f"  Validation set: {len(self.X_val):,} samples ({len(self.X_val)/len(self.X)*100:.1f}%)")
        print(f"  Test set:       {len(self.X_test):,} samples ({len(self.X_test)/len(self.X)*100:.1f}%)")
        
    def train_models(self):
        """Train multiple models"""
        print("\n" + "="*60)
        print("TRAINING MODELS")
        print("="*60)
        
        # Define models
        self.models = {
            'Linear Regression': LinearRegression(),
            'Random Forest': RandomForestRegressor(
                n_estimators=100,
                max_depth=20,
                min_samples_split=5,
                random_state=self.random_state,
                n_jobs=-1
            ),
            'Gradient Boosting': GradientBoostingRegressor(
                n_estimators=100,
                max_depth=5,
                learning_rate=0.1,
                random_state=self.random_state
            ),
            'XGBoost': xgb.XGBRegressor(
                n_estimators=100,
                max_depth=7,
                learning_rate=0.1,
                random_state=self.random_state,
                n_jobs=-1
            )
        }
        
        # Train each model
        for name, model in self.models.items():
            print(f"\nTraining {name}...")
            model.fit(self.X_train, self.y_train)
            print(f"✓ {name} trained successfully")
            
    def evaluate_models(self):
        """Evaluate all trained models"""
        print("\n" + "="*60)
        print("MODEL EVALUATION")
        print("="*60)
        
        best_score = -np.inf
        
        for name, model in self.models.items():
            # Predictions
            y_train_pred = model.predict(self.X_train)
            y_val_pred = model.predict(self.X_val)
            y_test_pred = model.predict(self.X_test)
            
            # Calculate metrics
            results = {
                'train_mae': mean_absolute_error(self.y_train, y_train_pred),
                'train_rmse': np.sqrt(mean_squared_error(self.y_train, y_train_pred)),
                'train_r2': r2_score(self.y_train, y_train_pred),
                'val_mae': mean_absolute_error(self.y_val, y_val_pred),
                'val_rmse': np.sqrt(mean_squared_error(self.y_val, y_val_pred)),
                'val_r2': r2_score(self.y_val, y_val_pred),
                'test_mae': mean_absolute_error(self.y_test, y_test_pred),
                'test_rmse': np.sqrt(mean_squared_error(self.y_test, y_test_pred)),
                'test_r2': r2_score(self.y_test, y_test_pred)
            }
            
            self.results[name] = results
            
            # Track best model based on validation R2
            if results['val_r2'] > best_score:
                best_score = results['val_r2']
                self.best_model = model
                self.best_model_name = name
            
            # Print results
            print(f"\n{name}:")
            print(f"  Train - MAE: {results['train_mae']:.3f}, RMSE: {results['train_rmse']:.3f}, R²: {results['train_r2']:.4f}")
            print(f"  Val   - MAE: {results['val_mae']:.3f}, RMSE: {results['val_rmse']:.3f}, R²: {results['val_r2']:.4f}")
            print(f"  Test  - MAE: {results['test_mae']:.3f}, RMSE: {results['test_rmse']:.3f}, R²: {results['test_r2']:.4f}")
        
        print(f"\n{'='*60}")
        print(f"🏆 BEST MODEL: {self.best_model_name}")
        print(f"   Validation R²: {self.results[self.best_model_name]['val_r2']:.4f}")
        print("="*60)
        
    def plot_results(self):
        """Visualize model performance"""
        
        # Prepare data for plotting
        metrics_df = pd.DataFrame(self.results).T
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # 1. R² Score comparison
        r2_data = metrics_df[['train_r2', 'val_r2', 'test_r2']]
        r2_data.plot(kind='bar', ax=axes[0, 0], color=['blue', 'orange', 'green'])
        axes[0, 0].set_title('R² Score Comparison', fontsize=14, fontweight='bold')
        axes[0, 0].set_ylabel('R² Score')
        axes[0, 0].set_xlabel('Model')
        axes[0, 0].legend(['Train', 'Validation', 'Test'])
        axes[0, 0].tick_params(axis='x', rotation=45)
        axes[0, 0].grid(True, alpha=0.3)
        
        # 2. MAE comparison
        mae_data = metrics_df[['train_mae', 'val_mae', 'test_mae']]
        mae_data.plot(kind='bar', ax=axes[0, 1], color=['blue', 'orange', 'green'])
        axes[0, 1].set_title('Mean Absolute Error Comparison', fontsize=14, fontweight='bold')
        axes[0, 1].set_ylabel('MAE')
        axes[0, 1].set_xlabel('Model')
        axes[0, 1].legend(['Train', 'Validation', 'Test'])
        axes[0, 1].tick_params(axis='x', rotation=45)
        axes[0, 1].grid(True, alpha=0.3)
        
        # 3. RMSE comparison
        rmse_data = metrics_df[['train_rmse', 'val_rmse', 'test_rmse']]
        rmse_data.plot(kind='bar', ax=axes[1, 0], color=['blue', 'orange', 'green'])
        axes[1, 0].set_title('Root Mean Squared Error Comparison', fontsize=14, fontweight='bold')
        axes[1, 0].set_ylabel('RMSE')
        axes[1, 0].set_xlabel('Model')
        axes[1, 0].legend(['Train', 'Validation', 'Test'])
        axes[1, 0].tick_params(axis='x', rotation=45)
        axes[1, 0].grid(True, alpha=0.3)
        
        # 4. Predicted vs Actual (best model)
        y_pred = self.best_model.predict(self.X_test)
        axes[1, 1].scatter(self.y_test, y_pred, alpha=0.5, s=10)
        axes[1, 1].plot([self.y_test.min(), self.y_test.max()], 
                       [self.y_test.min(), self.y_test.max()], 
                       'r--', lw=2, label='Perfect Prediction')
        axes[1, 1].set_title(f'Predicted vs Actual - {self.best_model_name}', 
                            fontsize=14, fontweight='bold')
        axes[1, 1].set_xlabel('Actual Congestion Score')
        axes[1, 1].set_ylabel('Predicted Congestion Score')
        axes[1, 1].legend()
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('models/model_comparison.png', dpi=300, bbox_inches='tight')
        print("\n✓ Comparison plot saved to models/model_comparison.png")
        plt.show()
        
    def plot_feature_importance(self, top_n=20):
        """Plot feature importance for tree-based models"""
        
        if self.best_model_name in ['Random Forest', 'Gradient Boosting', 'XGBoost']:
            # Get feature importance
            if hasattr(self.best_model, 'feature_importances_'):
                importance = self.best_model.feature_importances_
                feature_names = self.X.columns
                
                # Create dataframe
                importance_df = pd.DataFrame({
                    'feature': feature_names,
                    'importance': importance
                }).sort_values('importance', ascending=False).head(top_n)
                
                # Plot
                fig, ax = plt.subplots(figsize=(10, 8))
                importance_df.plot(x='feature', y='importance', kind='barh', ax=ax, 
                                  color='steelblue', legend=False)
                ax.set_title(f'Top {top_n} Feature Importances - {self.best_model_name}', 
                            fontsize=14, fontweight='bold')
                ax.set_xlabel('Importance')
                ax.set_ylabel('Feature')
                ax.invert_yaxis()
                
                plt.tight_layout()
                plt.savefig('models/feature_importance.png', dpi=300, bbox_inches='tight')
                print("✓ Feature importance plot saved to models/feature_importance.png")
                plt.show()
        else:
            print(f"Feature importance not available for {self.best_model_name}")
    
    def save_best_model(self, filepath='models/best_model.pkl'):
        """Save the best performing model"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        joblib.dump(self.best_model, filepath)
        
        # Save model info
        model_info = {
            'model_name': self.best_model_name,
            'metrics': self.results[self.best_model_name],
            'training_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'n_features': self.X.shape[1],
            'n_samples': len(self.X)
        }
        joblib.dump(model_info, 'models/model_info.pkl')
        
        print(f"\n✓ Best model ({self.best_model_name}) saved to {filepath}")
        print("✓ Model info saved to models/model_info.pkl")


def main():
    """Main training pipeline"""
    
    print("="*60)
    print("TRAFFIC CONGESTION PREDICTION - MODEL TRAINING")
    print("="*60)
    
    # Initialize predictor
    predictor = TrafficPredictor(random_state=42)
    
    # Load data
    predictor.load_data()
    
    # Split data
    predictor.split_data(test_size=0.2, val_size=0.1)
    
    # Train models
    predictor.train_models()
    
    # Evaluate models
    predictor.evaluate_models()
    
    # Plot results
    predictor.plot_results()
    
    # Plot feature importance
    predictor.plot_feature_importance(top_n=20)
    
    # Save best model
    predictor.save_best_model()
    
    print("\n" + "="*60)
    print("TRAINING COMPLETE!")
    print("="*60)
    print("\nNext steps:")
    print("  1. Review model performance metrics")
    print("  2. Check feature importance plot")
    print("  3. Proceed to API development")
    print("="*60)


if __name__ == "__main__":
    main()