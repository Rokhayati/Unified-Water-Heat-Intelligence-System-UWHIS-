import pandas as pd
import numpy as np
from datetime import datetime

def business_as_usual_scenario():
    """Data for the inefficient current system"""
    return {
        'scenario_name': 'Business as Usual',
        'water_efficiency': 65,  # percentage
        'energy_consumption': 850,  # MW
        'temperature_reduction': 2,  # degrees
        'water_distribution': {
            'residential': 45,
            'agricultural': 40,
            'industrial': 15
        },
        'renewable_energy_usage': 15,  # percentage
        'total_water_used': '1,200,000 L/day',
        'cost_per_day': 'AED 45,000',
        'status_messages': [
            "⚠️ High water waste in agricultural sector (40% loss)",
            "⚠️ Cooling systems operating at peak capacity", 
            "⚠️ No predictive optimization - reactive only",
            "⚠️ Grid dependency: 85% fossil fuels",
            "⚠️ Temperature hotspots detected in 8 zones"
        ],
        'color': 'red'
    }

def uwhis_activated_scenario():
    """Data for when UWHIS is active"""
    return {
        'scenario_name': 'UWHIS Activated',
        'water_efficiency': 88,  # percentage
        'energy_consumption': 620,  # MW
        'temperature_reduction': 8,  # degrees
        'water_distribution': {
            'residential': 40,  # Optimized
            'agricultural': 35,  # Reduced waste
            'industrial': 25    # Better allocation
        },
        'renewable_energy_usage': 65,  # percentage
        'total_water_used': '850,000 L/day',
        'cost_per_day': 'AED 28,500',
        'status_messages': [
            "✅ AI predicting water demand 24h ahead",
            "✅ Smart irrigation reducing waste by 30%",
            "✅ Renewable energy powering 65% of systems",
            "✅ Dynamic cooling: Heat zones reduced by 40%",
            "✅ Integrated optimization saving AED 16,500/day"
        ],
        'color': 'green'
    }

def get_demo_zone_data():
    """Get data for our demo zones"""
    zones = {
        'downtown': {
            'name': 'Downtown District',
            'temperature': 42.5,
            'water_demand': 450000,
            'cooling_need': 'High',
            'interventions': ['Smart misting', 'Shaded pavements', 'Building cooling']
        },
        'agricultural': {
            'name': 'Agricultural Zone A',
            'temperature': 38.0,
            'water_demand': 800000,
            'cooling_need': 'Medium',
            'interventions': ['Drip irrigation', 'Soil moisture sensors', 'Evening watering']
        },
        'residential': {
            'name': 'Residential Complex',
            'temperature': 40.0,
            'water_demand': 350000,
            'cooling_need': 'High',
            'interventions': ['Smart meters', 'Leak detection', 'Peak shifting']
        }
    }
    return zones

def calculate_benefits():
    """Calculate benefits of UWHIS"""
    baseline = business_as_usual_scenario()
    optimized = uwhis_activated_scenario()
    
    benefits = {
        'water_savings': f"{(optimized['water_efficiency'] - baseline['water_efficiency'])}%",
        'energy_savings': f"{(baseline['energy_consumption'] - optimized['energy_consumption'])} MW",
        'cost_savings': f"AED {16500}/day",
        'co2_reduction': '45 tons/day',
        'temperature_reduction': f"{optimized['temperature_reduction'] - baseline['temperature_reduction']}°C"
    }
    
    return benefits

# Test the functions
if __name__ == "__main__":
    print("🔧 Testing scenarios...")
    print("Business as usual:", business_as_usual_scenario()['scenario_name'])
    print("UWHIS Activated:", uwhis_activated_scenario()['scenario_name'])
    print("Demo zones:", list(get_demo_zone_data().keys()))
    print("✅ All scenarios working!")