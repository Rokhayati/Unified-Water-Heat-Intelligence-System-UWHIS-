import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta

def generate_synthetic_data():
    """Generate realistic synthetic data for Dubai simulation"""
    np.random.seed(42)  # For reproducible results
    
    # Generate 7 days of hourly data
    dates = pd.date_range('2024-01-15', periods=168, freq='H')
    
    # Create realistic temperature pattern (hot during day, cooler at night)
    base_temp = 35
    daily_cycle = 8 * np.sin(2 * np.pi * np.arange(168) / 24 - np.pi/2)
    temp_noise = np.random.normal(0, 2, 168)
    temperatures = base_temp + daily_cycle + temp_noise
    
    # Water demand increases with temperature
    base_water = 1000
    water_demand = base_water + temperatures * 25 + np.random.normal(0, 50, 168)
    
    # Split into sectors
    residential_share = 0.45  # 45%
    agricultural_share = 0.35  # 35%
    industrial_share = 0.20    # 20%
    
    synthetic_data = pd.DataFrame({
        'timestamp': dates,
        'temperature': temperatures,
        'total_water_demand': water_demand,
        'residential_water': water_demand * residential_share,
        'agricultural_water': water_demand * agricultural_share,
        'industrial_water': water_demand * industrial_share,
        'solar_power': 300 + 200 * np.sin(2 * np.pi * np.arange(168) / 24),  # More solar during day
        'energy_consumption': 500 + temperatures * 10
    })
    
    return synthetic_data

def predict_water_demand(temperature, time_of_day, day_type='weekday'):
    """Predict water demand based on conditions"""
    # Base model - you can make this more sophisticated
    base_demand = 1000
    
    # Temperature effect (more heat = more water needed)
    temp_effect = temperature * 25
    
    # Time of day effect (peak usage times)
    if 7 <= time_of_day <= 9:  # Morning peak
        time_effect = 300
    elif 18 <= time_of_day <= 21:  # Evening peak
        time_effect = 400
    else:
        time_effect = 0
    
    # Day type effect
    if day_type == 'weekend':
        day_effect = 200
    else:
        day_effect = 0
    
    predicted_demand = base_demand + temp_effect + time_effect + day_effect
    
    # Add some randomness for realism
    predicted_demand += np.random.normal(0, 50)
    
    return int(predicted_demand)

def calculate_water_savings(uwhis_active=True):
    """Calculate water savings from UWHIS"""
    if uwhis_active:
        return {
            'agricultural_savings': '35%',
            'residential_savings': '20%',
            'industrial_savings': '15%',
            'total_water_saved': '800,000 L/day'
        }
    else:
        return {
            'agricultural_savings': '0%',
            'residential_savings': '0%',
            'industrial_savings': '0%',
            'total_water_saved': '0 L/day'
        }

# Generate and save the data
if __name__ == "__main__":
    data = generate_synthetic_data()
    data.to_csv('data/synthetic_data.csv', index=False)
    print("✅ Data generated successfully!")
    print(f"📊 Data shape: {data.shape}")
    print(f"📅 Date range: {data['timestamp'].min()} to {data['timestamp'].max()}")
    print(f"🔥 Max temperature: {data['temperature'].max():.1f}°C")
    print(f"💧 Average water demand: {data['total_water_demand'].mean():.0f} L/hour")